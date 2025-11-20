# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from html.parser import HTMLParser
from urllib.parse import parse_qs, urlparse

import pytest
import requests
from keycloak import KeycloakAdmin
from keycloak.exceptions import KeycloakError

from e2e.keycloak import KeycloakDeployment
from e2e.kubernetes import KubernetesCluster

TEST_CLIENT_SECRET = "my-cache-test-secret"
TEST_REDIRECT_URI = "http://localhost:18888/callback"


class FormActionExtractionParser(HTMLParser):
    """HTML parser to extract the form action URL from Keycloak's login page."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.action_url: str | None = None

    def handle_starttag(self, tag, attrs: list[tuple[str, str | None]]):
        """Extract the action URL from the Keycloak login form."""
        if tag == "form":
            if any(attr[0] == "id" and attr[1] == "kc-form-login" for attr in attrs):
                self.action_url = next(attr[1] for attr in attrs if attr[0] == "action")


@pytest.fixture
def cache_test_client(keycloak_admin: KeycloakAdmin):
    """Create a test OIDC client for cache validation."""
    client_id = "cache-test-client"

    client_payload = {
        "clientId": client_id,
        "enabled": True,
        "protocol": "openid-connect",
        "publicClient": False,
        "standardFlowEnabled": True,
        "directAccessGrantsEnabled": False,
        "implicitFlowEnabled": False,
        "serviceAccountsEnabled": False,
        "redirectUris": [TEST_REDIRECT_URI],
        "attributes": {
            "pkce.code.challenge.method": "",
        },
        "secret": TEST_CLIENT_SECRET,
    }

    try:
        keycloak_admin.create_client(client_payload)
    except KeycloakError as e:
        if e.response_code != 409:
            raise

    yield client_id

    try:
        clients = keycloak_admin.get_clients()
        client = next((c for c in clients if c["clientId"] == client_id), None)
        if client:
            keycloak_admin.delete_client(client["id"])
    except Exception:
        pass


def extract_form_action_url(html: str) -> str:
    parser = FormActionExtractionParser()
    parser.feed(html)
    assert parser.action_url, f"Could not find login form in response: {html}"
    return parser.action_url


def rewrite_url_to_pod(url: str, target_port: int) -> str:
    """Rewrite a Keycloak URL to point to a specific pod via port-forward."""
    parsed = urlparse(url)
    return parsed._replace(scheme="http", netloc=f"127.0.0.1:{target_port}").geturl()


def initiate_auth_flow(session: requests.Session, keycloak_port: int, client_id: str) -> str:
    """
    Initiate OIDC authorization flow and return the login form action URL.

    Returns the form action URL from the login page.
    """
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": TEST_REDIRECT_URI,
    }
    resp = session.get(
        f"http://127.0.0.1:{keycloak_port}/realms/nubus/protocol/openid-connect/auth",
        params=params,
        allow_redirects=False,
    )

    # Clear secure flag on cookies to allow sending them over the HTTP port-forwards
    for cookie in session.cookies:
        cookie.secure = False

    assert resp.status_code == 200, f"Failed to initiate auth flow: {resp.text}"

    return extract_form_action_url(resp.text)


def submit_login(
    session: requests.Session,
    login_url: str,
    username: str,
    password: str,
) -> str:
    """
    Submit login credentials and return the authorization code.

    This is the step for testing cache replication - if the auth session
    is not in the distributed cache, this will fail.
    """
    resp = session.post(
        login_url,
        data={"username": username, "password": password},
        allow_redirects=False,
    )

    assert resp.status_code == 302, f"Login failed. If cache is not working, this will fail. Response: {resp.text}"

    location_header = resp.headers.get("location")
    assert location_header, "No location header in login response"

    parsed_location = urlparse(location_header)
    querystring = parse_qs(parsed_location.query)
    assert "code" in querystring, f"No authorization code in redirect: {location_header}"

    return querystring["code"][0]


def exchange_code_for_token(
    session: requests.Session,
    keycloak_port: int,
    code: str,
    client_id: str,
    client_secret: str,
) -> dict:
    """Exchange authorization code for access token."""
    token_params = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": TEST_REDIRECT_URI,
        "client_id": client_id,
        "client_secret": client_secret,
    }

    resp = session.post(
        f"http://127.0.0.1:{keycloak_port}/realms/nubus/protocol/openid-connect/token",
        data=token_params,
    )

    assert resp.status_code == 200, f"Token exchange failed: {resp.text}"
    token_response = resp.json()
    assert "access_token" in token_response, "No access token in response"

    return token_response


@pytest.mark.portal
@pytest.mark.acceptance_environment
def test_keycloak_cache(
    keycloak: KeycloakDeployment,
    k8s_supporting_port_forward: KubernetesCluster,
    cache_test_client: str,
    user,
    user_password: str,
):
    """
    Test Keycloak's Infinispan replication across replicas.

    This test validates that authentication sessions are properly replicated
    between Keycloak pods via the distributed cache. Authentication sessions
    are not persisted to the database unlike user sessions in KC26+, so
    they must be replicated via Infinispan for the cluster to work correctly.
    """

    if keycloak.num_keycloak_replicas() < 2:
        pytest.skip("Test requires at least 2 Keycloak replicas")

    keycloak_pods = keycloak.get_pods()
    assert len(keycloak_pods) >= 2, "Expected at least 2 Keycloak pods"

    keycloak_1_port = k8s_supporting_port_forward.port_forward_if_needed(keycloak_pods[0], 8080)[1]
    keycloak_2_port = k8s_supporting_port_forward.port_forward_if_needed(keycloak_pods[1], 8080)[1]

    session = requests.Session()
    username = user.properties["username"]

    form_action_url = initiate_auth_flow(session, keycloak_1_port, cache_test_client)

    login_url_on_pod2 = rewrite_url_to_pod(form_action_url, keycloak_2_port)
    code = submit_login(session, login_url_on_pod2, username, user_password)

    token_response = exchange_code_for_token(session, keycloak_1_port, code, cache_test_client, TEST_CLIENT_SECRET)

    assert token_response["access_token"]
    assert token_response["token_type"] == "Bearer"
