# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import pytest
from keycloak import KeycloakAdmin
from keycloak.openid_connection import KeycloakOpenIDConnection


@pytest.fixture
def auth_token(portal, keycloak, admin_username, admin_password, keycloak_admin: KeycloakAdmin):
    nubus_realm = keycloak_admin

    oidc_client = None
    for client in nubus_realm.get_clients():
        if client["clientId"] == f"{portal.base_url}univention/oidc/":
            oidc_client = client
            break

    assert oidc_client

    oidc_connection = KeycloakOpenIDConnection(
        server_url=keycloak.base_url,
        username=admin_username,
        password=admin_password,
        client_id=oidc_client["clientId"],
        client_secret_key=oidc_client["secret"],
        grant_type="password",
        realm_name="nubus",
        verify=True,
    )

    assert oidc_connection
    oidc_connection.get_token()

    return oidc_connection.token["access_token"]
