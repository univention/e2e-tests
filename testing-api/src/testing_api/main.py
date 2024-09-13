# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import logging
import socket
import time

import uvicorn
from fastapi import APIRouter, FastAPI

from testing_api.config import get_testing_api_settings
from testing_api.ldap_replication import check_replication_status
from testing_api.log import setup_logging

logger = logging.getLogger(__name__)


def resolve_pod_ips_from_headless_service(service_hostname: str) -> list[str]:
    address_info = socket.getaddrinfo(service_hostname, None)
    pod_ips = list(set((info[4][0] for info in address_info)))
    logger.debug("Resolved pod ips: %s from headless service hostname: %s.", pod_ips, service_hostname)
    return pod_ips


app = FastAPI()


testing_api_v1_router = APIRouter(prefix="/testing-api/v1")


@testing_api_v1_router.get("/ldap-replication-waiter")
async def ldap_replication_waiter(timeout: float | int = 10):
    start = time.perf_counter()
    logger.debug("Ensuring that the replication is in sync between the ldap primary and secondary")

    settings = get_testing_api_settings()

    ldap_secondary_ips = resolve_pod_ips_from_headless_service(settings.ldap_server_secondary_service_hostname)
    assert ldap_secondary_ips
    check_replication_status(timeout, ldap_secondary_ips, settings)

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

    ldap_secondary_ips = resolve_pod_ips_from_headless_service(settings.ldap_server_secondary_service_hostname)
    assert ldap_secondary_ips

    check_replication_status(1, ldap_secondary_ips, settings)
    logger.info("LDAP Connections are workind and replication status can be monitored.")


def main():
    settings = get_testing_api_settings()
    assert settings
    setup_logging(settings.log_level)

    uvicorn.run(app, host="0.0.0.0", port=4434, log_config=None)


if __name__ == "__main__":
    main()
