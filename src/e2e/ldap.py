# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import logging

from ldap3 import Connection, Server

from e2e.kubernetes import KubernetesCluster


log = logging.getLogger(__name__)


class LDAPServer:
    """
    Represents one LDAP server process / Pod in our deployment.
    """

    conn: Connection

    def __init__(self, name: str, host: str, port: int | None = None, client_strategy="SYNC"):
        self.name = name
        self.host = host
        self.port = port

        self._connect(client_strategy)

    def _connect(self, client_strategy):
        server = Server(
            host=self.host,
            port=self.port,
            get_info="ALL",
            connect_timeout=1,
        )
        self.conn = Connection(
            server,
            user="cn=admin,dc=univention-organization,dc=intranet",
            password="univention",
            client_strategy=client_strategy,
            raise_exceptions=True,
        )

    def get_context_csn(self) -> list[str]:
        context_csn = []
        try:
            with self.conn:
                self.conn.search(
                    "dc=univention-organization,dc=intranet",
                    "(objectClass=*)",
                    search_scope="BASE",
                    attributes=["contextCSN"],
                )
                context_csn = self.conn.entries[0].contextCSN.values
        except Exception:
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
    _next_local_port = 3890

    def __init__(self, k8s: KubernetesCluster):
        self._k8s = k8s
        servers = [
            LDAPServer(name="primary_0", host=self._uri_for_pod("ldap-server-primary-0")),
            LDAPServer(name="primary_1", host=self._uri_for_pod("ldap-server-primary-1")),
        ]
        self.servers = {server.name: server for server in servers}

    def _uri_for_pod(self, pod_name, target_type="pod"):
        host, port = self._k8s.port_forward_if_needed(
            target_name=pod_name,
            target_namespace="default",
            target_port=389,
            local_port=self._next_local_port,
            target_type=target_type,
        )
        self._next_local_port += 1
        return f"ldap://{host}:{port}"

    def all_primaries_reachable(self):
        for server in self.servers.values():
            log.debug("Checking reachability of server %s", server.name)
            try:
                with server.conn:
                    pass
            except Exception:
                log.debug("Server %s not reachable", server.name)
                return False
        return True

    def get_context_csn(self) -> dict[str, list[str]]:
        return {
            name: server.get_context_csn() for name, server in self.servers.items()
        }

    def get_server_for_primary_service(self, auto_reconnect=True) -> LDAPServer:
        role = "primary_service"
        if auto_reconnect:
            client_strategy = "RESTARTABLE"
        else:
            client_strategy = "SYNC"
        server = LDAPServer(
            name=role,
            host=self._uri_for_pod("ldap-server-primary", target_type="service"),
            client_strategy=client_strategy,
        )
        return server
