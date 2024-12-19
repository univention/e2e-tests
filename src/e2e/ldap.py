# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import logging

import ldap3.core.exceptions
from ldap3 import Connection, Server

from e2e.kubernetes import KubernetesCluster

log = logging.getLogger(__name__)


class LDAPServer:
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

    def __init__(self, name: str, host: str, port: int | None = None, client_strategy="SYNC"):
        self.name = name
        self.host = host
        self.port = port
        self.server = Server(host=self.host, port=self.port, get_info="ALL", connect_timeout=1)
        self.client_strategy = client_strategy

    def connect(self, bind=False, client_strategy=None):
        if not client_strategy:
            client_strategy = self.client_strategy
        connection = Connection(
            self.server,
            user="cn=admin,dc=univention-organization,dc=intranet",
            password="univention",
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
                    "dc=univention-organization,dc=intranet",
                    "(objectClass=*)",
                    search_scope="BASE",
                    attributes=["contextCSN"],
                )
                context_csn = conn.entries[0].contextCSN.values
        except ldap3.core.exceptions.LDAPException:
            log.debug("Reading contextCSN from server %s failed.", self.name)
        return context_csn


class LDAPFixture:
    """
    Represents the openldap deployment.

    It does map servers by "role" and a running number, so that the whole
    deployment could be represented, including the roles "primary", "secondary"
    and "proxy".
    """

    servers: dict[str, LDAPServer]

    def __init__(self, k8s: KubernetesCluster, release_name):
        self._k8s = k8s
        self.release_name = release_name
        primary_0 = self._apply_release_prefix("ldap-server-primary-0")
        primary_1 = self._apply_release_prefix("ldap-server-primary-1")
        servers = [
            LDAPServer(name="primary_0", host=self._uri_for_pod(primary_0)),
            LDAPServer(name="primary_1", host=self._uri_for_pod(primary_1)),
        ]
        self.servers = {server.name: server for server in servers}

    def _apply_release_prefix(self, name):
        if not self.release_name or self.release_name == name:
            return name
        return f"{self.release_name}-{name}"

    def _uri_for_pod(self, pod_name, target_type="pod"):
        host, port = self._k8s.port_forward_if_needed(
            target_name=pod_name,
            target_port=389,
            target_type=target_type,
        )
        return f"ldap://{host}:{port}"

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

    def get_server_for_primary_service(self, auto_reconnect=True) -> LDAPServer:
        role = "primary_service"
        if auto_reconnect:
            client_strategy = "RESTARTABLE"
        else:
            client_strategy = "SYNC"
        service_name = self._apply_release_prefix("ldap-server-primary")
        server = LDAPServer(
            name=role,
            host=self._uri_for_pod(service_name, target_type="service"),
            client_strategy=client_strategy,
        )
        return server
