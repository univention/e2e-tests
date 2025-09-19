# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import logging
import os
from base64 import b64decode

import ldap3.core.exceptions
from kubernetes import client
from ldap3 import Connection, Server

from e2e.base import BaseDeployment
from e2e.kubernetes import KubernetesCluster
from e2e.types import LdapDn

log = logging.getLogger(__name__)


DEFAULT_CLIENT_STRATEGY = ldap3.SYNC


class LdapServer:
    """
    Represents one LDAP server process / Pod in our deployment.

    The `client_stragety` parameter around the connections is important.
    Typically we use the following options:

    - `"SYNC"` is the default in use. This will fail if the connection cannot
      be established.

    - `"RESTARTABLE"` is useful in some scenarios. It will automatically try to
      re-establish the connection until an internal timeout.

    Regarding details see: https://ldap3.readthedocs.io/en/latest/connection.html
    """

    conn: Connection

    def __init__(
        self,
        name: str,
        host: str,
        bind_dn: str,
        bind_password: str,
        base_dn: str,
        port: int | None = None,
        client_strategy=DEFAULT_CLIENT_STRATEGY,
    ):
        self.name = name
        self.host = host
        self.port = port
        self.bind_dn = bind_dn
        self.bind_password = bind_password
        self.base_dn = base_dn
        self.server = Server(host=self.host, port=self.port, get_info="ALL", connect_timeout=1)
        self.client_strategy = client_strategy

    def connect(self, bind=False, client_strategy=None):
        if not client_strategy:
            client_strategy = self.client_strategy
        connection = Connection(
            self.server,
            user=self.bind_dn,
            password=self.bind_password,
            client_strategy=client_strategy,
            raise_exceptions=True,
        )
        if bind:
            connection.bind()
        return connection

    def get_context_csn(self) -> list[str]:
        context_csn = []
        try:
            with self.connect() as conn:
                conn.search(
                    self.base_dn,
                    "(objectClass=*)",
                    search_scope="BASE",
                    attributes=["contextCSN"],
                )
                context_csn = conn.entries[0].contextCSN.values
        except ldap3.core.exceptions.LDAPException:
            log.debug("Reading contextCSN from server %s failed.", self.name)
        return context_csn


class LdapDeployment(BaseDeployment):
    """
    Represents the openldap deployment.

    It does map servers by "role" and a running number, so that the whole
    deployment could be represented, including the roles "primary", "secondary"
    and "proxy".
    """

    admin_dn: LdapDn = None
    """The DN of the LDAP admin user."""

    admin_rdn = "cn=admin"
    """The RDN of the LDAP admin user."""

    admin_password: str = None
    """The password of the LDAP admin user."""

    servers: dict[str, LdapServer]

    LABELS_ACTIVE_PRIMARY_LDAP_SERVER = {
        "app.kubernetes.io/name": "ldap-server",
        "ldap-server-type": "primary",
        "ldap-leader": "true",
    }

    def __init__(self, k8s: KubernetesCluster, release_name: str):
        self._k8s = k8s
        self.release_name = release_name
        self.primary_0_pod_name = self.add_release_prefix("ldap-server-primary-0")
        self.primary_1_pod_name = self.add_release_prefix("ldap-server-primary-1")
        self.notifier_pod_name = self.add_release_prefix("ldap-notifier-0")
        self.notifier_stateful_set_name = self.add_release_prefix("ldap-notifier")
        self._discover_from_cluster()
        servers = [
            self._create_server("primary_0", self.primary_0_pod_name),
            self._create_server("primary_1", self.primary_1_pod_name),
        ]
        self.servers = {server.name: server for server in servers}

    def _discover_from_cluster(self):
        config_map_name = self.add_release_prefix("ldap-server")
        v1 = client.CoreV1Api()
        config_map = v1.read_namespaced_config_map(
            name=config_map_name,
            namespace=self._k8s.namespace,
        )

        self.base_dn = config_map.data["LDAP_BASE_DN"]
        self.admin_dn = f"cn=admin,{self.base_dn}"
        self.users_container_dn = f"cn=users,{self.base_dn}"
        self.administrator_dn = f"uid=Administrator,{self.users_container_dn}"

        secret_name = os.getenv("LDAP_CREDENTIALS_SECRET_NAME", self.add_release_prefix("ldap-server-admin"))
        secret_key = os.getenv("LDAP_CREDENTIALS_SECRET_KEY", "password")

        secret = self._k8s.get_secret(secret_name)
        self.admin_password = b64decode(secret.data[secret_key]).decode()

    def all_primaries_reachable(self):
        for server in self.servers.values():
            log.debug("Checking reachability of server %s", server.name)
            try:
                with server.connect():
                    pass
            except Exception:
                log.debug("Server %s not reachable", server.name)
                return False
        return True

    def get_context_csn(self) -> dict[str, list[str]]:
        return {name: server.get_context_csn() for name, server in self.servers.items()}

    def get_server_for_primary_service(self, auto_reconnect=True) -> LdapServer:
        role = "primary_service"
        if auto_reconnect:
            client_strategy = ldap3.RESTARTABLE
        else:
            client_strategy = DEFAULT_CLIENT_STRATEGY
        service_name = self.add_release_prefix("ldap-server-primary")
        server = self._create_server(
            name=role,
            pod_name=service_name,
            client_strategy=client_strategy,
            target_type="service",
        )
        return server

    def _create_server(
        self,
        name,
        pod_name,
        client_strategy=DEFAULT_CLIENT_STRATEGY,
        target_type="pod",
    ) -> LdapServer:
        server = LdapServer(
            name=name,
            host=self._uri_for_pod(pod_name, target_type),
            bind_dn=self.admin_dn,
            bind_password=self.admin_password,
            base_dn=self.base_dn,
            client_strategy=client_strategy,
        )
        return server

    def _uri_for_pod(self, pod_name, target_type="pod"):
        host, port = self._k8s.port_forward_if_needed(
            target_name=pod_name,
            target_port=389,
            target_type=target_type,
        )
        return f"ldap://{host}:{port}"
