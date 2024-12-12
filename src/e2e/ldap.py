# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import logging
import time

from ldap3 import Connection, Server


log = logging.getLogger(__name__)


class LDAPServer:
    """
    Represents one LDAP server process / Pod in our deployment.
    """

    conn: Connection

    def __init__(self, name: str, host: str, port: int, client_strategy="SYNC"):
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

    def __init__(self):
        servers = [
            LDAPServer(name="primary_1", host="ldap://localhost", port=8389),
            LDAPServer(name="primary_0", host="ldap://localhost", port=9389),
        ]
        self.servers = {server.name: server for server in servers}

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

    def get_server(self, role: str, auto_reconnect=True) -> LDAPServer:
        if auto_reconnect:
            client_strategy = "RESTARTABLE"
        else:
            client_strategy = "SYNC"
        server = LDAPServer(
            name=role,
            host="ldap://localhost",
            port=7389,
            client_strategy=client_strategy,
        )
        return server
