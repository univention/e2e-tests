# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import logging
import socket
import time

import uvicorn
from fastapi import APIRouter, FastAPI, HTTPException
from ldap3.core.exceptions import LDAPSocketOpenError, LDAPSocketReceiveError

from testing_api.config import get_testing_api_settings
from testing_api.ldap_replication import BetterRetryError, check_replication_status
from testing_api.log import setup_logging

logger = logging.getLogger(__name__)


def resolve_pod_ips_from_headless_service(service_hostname: str) -> list[str]:
    address_info = socket.getaddrinfo(service_hostname, None)
    pod_ips = list(set((info[4][0] for info in address_info)))
    logger.debug("Resolved pod ips: %s from headless service hostname: %s.", pod_ips, service_hostname)
    return pod_ips


def exception_logger(exc: Exception) -> None:
    logger.debug("Exception occurred", exc_info=exc)
    logger.info("Exception: %s", str(exc))


app = FastAPI()


testing_api_v1_router = APIRouter(prefix="/testing-api/v1")


@testing_api_v1_router.get("/ldap-replication-waiter", status_code=200)
async def ldap_replication_waiter(retry_timeout: float | int = 10):
    start = time.perf_counter()
    logger.debug("request query parameters: timeout=%s", retry_timeout)
    logger.debug("Ensuring that the replication is in sync between the ldap primary and secondary")

    settings = get_testing_api_settings()

    ldap_primary_ips = resolve_pod_ips_from_headless_service(settings.ldap_server_primary_service_hostname)
    try:
        ldap_secondary_ips = resolve_pod_ips_from_headless_service(settings.ldap_server_secondary_service_hostname)
    except socket.gaierror as exc:
        if ldap_primary_ips:
            logger.info(
                "Inferred that no LDAP Server secondaries are deployed. Skipping the replication check. request time: %.3f seconds",
                time.perf_counter() - start,
            )
            return True
        exception_logger(exc)
        raise HTTPException(status_code=503, detail="Failed to resolve ldap server secondary IP's")

    assert ldap_secondary_ips
    try:
        check_replication_status(retry_timeout, ldap_secondary_ips, settings)
    except BetterRetryError as exc:
        exception_logger(exc)
        raise HTTPException(
            status_code=409, detail=f"Not all secondaries have caught up within the timeout of {retry_timeout}s"
        )
    except (LDAPSocketOpenError, LDAPSocketReceiveError) as exc:
        exception_logger(exc)
        raise HTTPException(status_code=503, detail="Failed to establish a connection to one of the ldap servers")
    logger.info(
        "All LDAP Secondarys have caught up with the Primary at the start of this request. request time: %.3f seconds",
        time.perf_counter() - start,
    )

    return True


app.include_router(testing_api_v1_router)


@app.on_event("startup")
async def startup_task():
    logger.info("Started %s.", app.title)
    for route in app.routes:
        logger.debug("API route: %s", route)

    settings = get_testing_api_settings()

    ldap_primary_ips = resolve_pod_ips_from_headless_service(settings.ldap_server_primary_service_hostname)
    try:
        ldap_secondary_ips = resolve_pod_ips_from_headless_service(settings.ldap_server_secondary_service_hostname)
    except socket.gaierror:
        if ldap_primary_ips:
            logger.info("Inferred that no LDAP Server secondaries are deployed. Skipping the replication check")
            return
        raise

    ldap_secondary_ips = resolve_pod_ips_from_headless_service(settings.ldap_server_secondary_service_hostname)
    assert ldap_secondary_ips
    try:
        check_replication_status(1, ldap_secondary_ips, settings)
        pass
    except BetterRetryError:
        logger.debug("Ldap replication is out of sync but the startup task still verified that it can be monitored")
    logger.info("LDAP Connections are workind and replication status can be monitored.")


def main():
    settings = get_testing_api_settings()
    assert settings
    setup_logging(settings.log_level)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=4434,
        log_config=None,
    )


if __name__ == "__main__":
    main()
