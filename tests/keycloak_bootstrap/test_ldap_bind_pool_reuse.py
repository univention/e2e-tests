# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2026 Univention GmbH

"""
Test for Keycloak LDAP federation connection pooling.

This test verify that Keycloak reuses a single pooled, already-bound
LDAP service-account connection across federated user logins, instead
of rebinding the service account on every operation
"""

import logging
import re
import time
from collections import Counter

import pytest
from keycloak.openid_connection import KeycloakOpenIDConnection

logger = logging.getLogger(__name__)

pytestmark = [
    pytest.mark.development_environment,
    pytest.mark.acceptance_environment,
]

LOGINS = 15
MAX_BINDS_PER_CONNECTION = 1


def _ldap_federation_config(keycloak_admin) -> dict | None:
    for component in keycloak_admin.get_components():
        if component.get("providerType") == "org.keycloak.storage.UserStorageProvider":
            config = component.get("config", {})
            if config.get("bindDn"):
                return config
    return None


def _config_flag(config: dict, key: str) -> bool:
    return config.get(key, ["false"])[0] == "true"


def _direct_grant_client(keycloak_admin, portal) -> dict:
    client_id = f"{portal.base_url}univention/oidc/"
    for client in keycloak_admin.get_clients():
        if client["clientId"] == client_id:
            if not (client.get("directAccessGrantsEnabled") and client.get("secret")):
                pytest.skip(f"Client {client_id} cannot drive direct-grant logins")
            return client
    pytest.skip(f"No direct-access-grant client {client_id!r} found")


def _binds_per_connection(k8s, bind_dn, since_seconds) -> Counter:
    # Connection ids are unique only within a single slapd, so namespace them by pod.
    bind_line = re.compile(
        rf'conn=(\d+)\s+op=\d+\s+BIND dn="{re.escape(bind_dn)}"\s+mech=SIMPLE',
        re.IGNORECASE,
    )
    pods = k8s._get_pods_from_match_labels({"app.kubernetes.io/name": "ldap-server"}, namespace=k8s.namespace)
    binds: Counter = Counter()
    for pod in pods.items:
        logs = k8s.check_pod_logs(pod_name=pod.metadata.name, container_name="main", since_seconds=since_seconds)
        for conn_id in bind_line.findall(logs or ""):
            binds[f"{pod.metadata.name}:conn={conn_id}"] += 1
    return binds


class TestKeycloakLdapBindPoolReuse:
    def test_service_account_connection_is_reused_across_logins(
        self, ldap_test_user, keycloak, keycloak_admin, k8s, portal
    ):
        config = _ldap_federation_config(keycloak_admin)
        if config is None:
            pytest.skip("No LDAP user-federation provider with a bindDn configured")

        if not _config_flag(config, "connectionPooling") or _config_flag(config, "startTls"):
            pytest.skip("LDAP federation does not use pooled, non-StartTLS connections; regression does not apply")

        bind_dn = config["bindDn"][0]
        client = _direct_grant_client(keycloak_admin, portal)

        def login():
            connection = KeycloakOpenIDConnection(
                server_url=keycloak.base_url,
                username=ldap_test_user["username"],
                password=ldap_test_user["password"],
                client_id=client["clientId"],
                client_secret_key=client["secret"],
                grant_type="password",
                realm_name="nubus",
                verify=True,
            )
            connection.get_token()
            assert connection.token.get("access_token"), "login did not return an access token"

        start = time.monotonic()
        for _ in range(LOGINS):
            login()

        # Only read the LDAP logs produced by the logins above, so the count is
        # attributable to this test rather than to an arbitrary tail length.
        binds = _binds_per_connection(k8s, bind_dn, since_seconds=int(time.monotonic() - start) + 5)
        busiest_connection, max_binds = binds.most_common(1)[0] if binds else ("none", 0)

        logger.info("service-account (%s) binds per LDAP connection: %r", bind_dn, dict(binds))
        assert max_binds <= MAX_BINDS_PER_CONNECTION, (
            f"{bind_dn} was re-bound {max_binds}x on a single pooled connection ({busiest_connection}); "
            f"a pooled, already-bound connection must be reused without re-binding (keycloak#50201)"
        )
