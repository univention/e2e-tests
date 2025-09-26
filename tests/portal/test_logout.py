# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from typing import Any

import pytest
import requests
import yaml
from keycloak import KeycloakAdmin
from playwright.sync_api import BrowserContext

from e2e.keycloak import KeycloakDeployment
from e2e.kubernetes import KubernetesCluster
from umspages.portal.home_page.logged_in import HomePageLoggedIn
from umspages.portal.home_page.logged_out import HomePageLoggedOut


@pytest.fixture(scope="session")
def oidc_well_known(keycloak: KeycloakDeployment):
    realm = "nubus"
    well_known_url = f"{keycloak.base_url}/realms/{realm}/.well-known/openid-configuration"
    well_known_response = requests.get(well_known_url)
    assert well_known_response.status_code == 200

    return well_known_response.json()


@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
@pytest.mark.usefixtures("update_keycloak_backchannel_logout_url")
def test_refresh_on_backchannel_logout(context: BrowserContext, user, user_password, oidc_well_known: dict[str, Any]):
    portal_page = context.new_page()
    logout_page = context.new_page()
    home_page_logged_in = HomePageLoggedIn(portal_page)
    username = user.properties["username"]
    home_page_logged_in.navigate(username, user_password)

    end_session_endpoint = oidc_well_known["end_session_endpoint"]

    logout_page.goto(end_session_endpoint)
    logout_page.get_by_role("button", name="Logout").click()

    home_page_logged_out = HomePageLoggedOut(portal_page)
    home_page_logged_out.assert_logged_out()


@pytest.fixture
def remove_umc_server(k8s: KubernetesCluster, release_name: str):
    cm_name = f"{release_name}-umc-server-proxy"
    cm = k8s.get_configmap(cm_name)
    traefik_dynamic_config_cm_data = cm.data["dynamic.yaml"]

    traefik_dynamic_config = yaml.load(traefik_dynamic_config_cm_data, Loader=yaml.CLoader)
    umc_servers: list[dict[str, Any]] = traefik_dynamic_config["http"]["services"]["umc-server"]["loadBalancer"][
        "servers"
    ]

    if len(umc_servers) == 1:
        yield None
        return

    removed_umc_server = umc_servers.pop()

    updated_traefik_dynamic_config = yaml.dump(traefik_dynamic_config, Dumper=yaml.CDumper)
    k8s.update_configmap_data("dynamic.yaml", updated_traefik_dynamic_config, cm_name)
    restart_umc_traefik_proxy(k8s, release_name)

    yield removed_umc_server["url"]

    k8s.update_configmap_data("dynamic.yaml", traefik_dynamic_config_cm_data, cm_name)
    restart_umc_traefik_proxy(k8s, release_name)


def restart_umc_traefik_proxy(k8s: KubernetesCluster, release_name: str):
    umc_server_proxy_pods = k8s.get_pod_names_for_deployment(f"{release_name}-umc-server")
    for umc_server_proxy_pod in umc_server_proxy_pods:
        k8s.delete_pod(umc_server_proxy_pod)


@pytest.fixture
def update_keycloak_backchannel_logout_url(keycloak_admin: KeycloakAdmin, remove_umc_server: str | None):
    if remove_umc_server is None:
        return

    clients = keycloak_admin.get_clients()

    umc_oidc_client = next((client for client in clients if client["name"] == "UMC OIDC"), None)
    assert umc_oidc_client, f"UMC OIDC client not found in Keycloak realm {keycloak_admin.get_current_realm()}"
    umc_oidc_client_id = umc_oidc_client["id"]

    old_backchannel_logout_url = umc_oidc_client["attributes"]["backchannel.logout.url"]
    new_backchannel_logout_url = f"{remove_umc_server}/oidc/backchannel-logout"
    update_backchannel_logout_url(umc_oidc_client_id, new_backchannel_logout_url, keycloak_admin)

    yield

    update_backchannel_logout_url(umc_oidc_client_id, old_backchannel_logout_url, keycloak_admin)


def update_backchannel_logout_url(client_id: str, backchannel_logout_url: str, keycloak_admin: KeycloakAdmin):
    client_restore_payload = {"attributes": {"backchannel.logout.url": backchannel_logout_url}}

    keycloak_admin.update_client(client_id, client_restore_payload)
