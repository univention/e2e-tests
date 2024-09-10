# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import logging

from ldap3 import ALL, Connection, Server
from tenacity import RetryError, before_sleep_log, retry, stop_after_delay, wait_fixed

from testing_api.config import TestingApiSettings

logger = logging.getLogger(__name__)


def create_connection(hostname: str, port: int, settings: TestingApiSettings) -> Connection:
    return Connection(
        Server(f"ldap://{hostname}:{port}", get_info=ALL),
        user=settings.ldap_bind_dn,
        password=settings.ldap_bind_password,
        auto_bind=True,
    )


def compare_context_csn(primary_server_csn: str, secondary_server_csn) -> bool:
    """
    contextCSN's have the following encoding: TIMESTAMP#COUNT#SID#MOD
    """
    try:
        old_timestamp, old_count, old_sid, old_mod = primary_server_csn.split("#")
        new_timestamp, new_count, new_sid, new_mod = secondary_server_csn.split("#")
    except ValueError:
        logger.error("Error while parsing contextCSN's. old: %s, new: %s", primary_server_csn, secondary_server_csn)
        raise

    if old_timestamp > new_timestamp:
        return False
    if old_timestamp < new_timestamp:
        return True
    if all((
        new_count == old_count,
        new_sid == old_sid,
        new_mod == old_mod,
    )):
        return True
    return False


def get_context_csn(connection: Connection, settings: TestingApiSettings):
    connection.search(settings.ldap_base_dn, "(objectClass=*)", attributes=["contextCSN"])
    result = connection.entries[0].contextCSN.value
    if not result:
        raise ValueError("No contextCSN in ldap search result")
    logger.debug("contextCSN for ldap server %s is: %s", connection.server.host, result)
    return result


def get_primary_csn(settings: TestingApiSettings) -> str:
    connection = create_connection(settings.ldap_server_primary_service_hostname, settings.ldap_server_primary_port, settings)
    try:
        return get_context_csn(connection, settings)
    finally:
        connection.unbind()


class BetterRetryError(RetryError):
    def __str__(self) -> str:
        start = f"attempt_number={self.last_attempt.attempt_number}, "
        end = f"failed={self.last_attempt.failed}, done={self.last_attempt.done()}, cancelled={self.last_attempt.cancelled()}"

        if (exception := self.last_attempt.exception()) is not None:
            result = f"{start}exception={exception}, exception_type={type(exception)}"
        else:
            result = f"{start}result={self.last_attempt.result()}"

        return (result + end).replace("\n", "; ")


def check_replication_status(timeout: float | int, ldap_secondary_ips: list[str], settings: TestingApiSettings):
    primary_csn = get_primary_csn(settings)
    assert primary_csn

    secondary_connections = [create_connection(ip, settings.ldap_server_secondary_port, settings) for ip in ldap_secondary_ips]

    @retry(
        stop=stop_after_delay(timeout),
        before_sleep=before_sleep_log(logger, logging.DEBUG),
        wait=wait_fixed(0.25),
        retry_error_cls=BetterRetryError,
    )
    def wait():
        for connection in secondary_connections:
            secondary_csn = get_context_csn(connection, settings)

            assert compare_context_csn(primary_csn, secondary_csn), "Replication is out of sync!"
    wait()
