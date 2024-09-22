# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings

Loglevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class TestingApiSettings(BaseSettings):
    log_level: Loglevel

    ldap_base_dn: str
    ldap_bind_dn: str
    ldap_bind_password: str
    ldap_server_primary_service_hostname: str
    ldap_server_primary_port: int
    ldap_server_secondary_service_hostname: str
    ldap_server_secondary_port: int

    nats_user: str
    nats_password: str
    nats_host: str
    nats_port: int

    @property
    def nats_server(self) -> str:
        return f"nats://{self.nats_host}:{self.nats_port}"


@lru_cache
def get_testing_api_settings() -> TestingApiSettings:
    return TestingApiSettings()
