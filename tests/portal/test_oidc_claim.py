# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import base64
import json
import logging

import pytest
import requests

from tests.portal.conftest import WaitForUserExists

logger = logging.getLogger(__name__)


@pytest.fixture
def user_mixed_case(
    udm, faker, email_domain, external_email_domain, user_password, wait_for_ldap_secondaries_to_catch_up
):
    """
    A regular user.

    The user will be created for the test case and removed after the test case.

    The password is available in the fixture ``user_password``.
    """
    users_user = udm.get("users/user")
    test_user = users_user.new()
    username = f"test-{faker.user_name()}".capitalize()

    test_user.properties.update(
        {
            "firstname": faker.first_name(),
            "lastname": faker.last_name(),
            "username": username,
            "displayName": faker.name(),
            "password": user_password,
            "mailPrimaryAddress": f"{username}@{email_domain}",
            "PasswordRecoveryEmail": f"{username}@{external_email_domain}",
        }
    )
    test_user.save()

    wait_for_ldap_secondaries_to_catch_up()
    yield test_user

    test_user.reload()
    test_user.delete()


# Decode JWT (ID token)
def decode_jwt_section(section):
    """Decode a JWT base64url-encoded section."""
    section += "=" * (-len(section) % 4)  # fix padding
    return base64.urlsafe_b64decode(section.encode())


def get_client_secret(keycloak, keycloak_admin_username, keycloak_admin_password, client):
    token_url = f"{keycloak}realms/master/protocol/openid-connect/token"

    token_data = {
        "grant_type": "password",
        "client_id": "admin-cli",
        "username": keycloak_admin_username,
        "password": keycloak_admin_password,
    }
    token_resp = requests.post(token_url, data=token_data)
    token_resp.raise_for_status()
    admin_access_token = token_resp.json()["access_token"]

    # Get client info by clientId
    clients_url = f"{keycloak}admin/realms/nubus/clients"
    headers = {"Authorization": f"Bearer {admin_access_token}"}

    params = {"clientId": client}
    clients_resp = requests.get(clients_url, headers=headers, params=params)
    clients_resp.raise_for_status()

    client_info = clients_resp.json()[0]  # first match
    client_uuid = client_info["id"]

    secret_url = f"{keycloak}admin/realms/nubus/clients/{client_uuid}/client-secret"

    secret_resp = requests.get(secret_url, headers=headers)
    secret_resp.raise_for_status()

    client_secret = secret_resp.json()["value"]

    return client_secret


def get_oidc_claim_sub(username, password, keycloak, keycloak_admin_username, keycloak_admin_password, portal):
    token_url = f"{keycloak.base_url}realms/nubus/protocol/openid-connect/token"
    client_id = f"{portal.base_url}univention/oidc/"
    client_secret = get_client_secret(keycloak.base_url, keycloak_admin_username, keycloak_admin_password, client_id)

    data = {
        "grant_type": "password",
        "client_id": client_id,
        "client_secret": client_secret,
        "username": username,
        "password": password,
        "scope": "openid",
    }

    response = requests.post(token_url, data=data)
    response.raise_for_status()
    tokens = response.json()

    id_token = tokens["id_token"]

    header_b64, payload_b64, signature_b64 = id_token.split(".")
    payload = json.loads(decode_jwt_section(payload_b64))

    # Extract sub claim
    sub = payload.get("sub")
    return sub


@pytest.mark.acceptance_environment
def test_oidc_claim_mixed_case(
    user_mixed_case,
    user_password,
    keycloak,
    keycloak_admin_username,
    keycloak_admin_password,
    portal,
    ensure_user_exists: WaitForUserExists,
):
    username = user_mixed_case.properties["username"]
    ensure_user_exists(username.lower())

    sub_username = get_oidc_claim_sub(
        username,
        user_password,
        keycloak,
        keycloak_admin_username,
        keycloak_admin_password,
        portal,
    )

    assert username in sub_username
