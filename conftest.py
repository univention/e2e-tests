# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import logging
import os
import random

import pytest

from e2e.keycloak import KeycloakDeployment
from e2e.kubernetes import KubernetesCluster
from e2e.ldap import LdapDeployment
from e2e.portal import PortalDeployment
from e2e.stack_data import StackDataDeployment
from e2e.udm import UdmRestApiDeployment

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    # Portal tests options
    parser.addoption("--portal-base-url", help="Override discovered base URL of the Univention Portal")
    parser.addoption("--admin-username", default="Administrator", help="Portal admin login username")
    parser.addoption("--admin-password", default="univention", help="Portal admin login password")
    parser.addoption("--email-test-api-username", default="user", help="Username to access the email test API.")
    parser.addoption("--email-test-api-password", default="univention", help="Password to access the email test API.")
    parser.addoption("--email-test-api-base-url", default="", help="Base URL to reach the email test API (Maildev).")
    parser.addoption(
        "--portal-central-navigation-secret",
        default="univention",
        help="Shared secret with portal-server for central navigation",
    )
    # BFP tests options
    parser.addoption("--keycloak-base-url", help="Base URL of Keycloak")
    parser.addoption("--kc-admin-username", default="admin", help="Keycloak admin login username")
    parser.addoption("--kc-admin-password", default="univention", help="Keycloak admin login password")
    parser.addoption("--num-device-block", type=int, default=5, help="Number of failed logins for device block")
    parser.addoption("--num-ip-block", type=int, default=7, help="Number of failed logins for IP block")
    parser.addoption("--release-duration", type=int, default=1, help="Blocks are released after this many minutes")
    parser.addoption("--realm", default="master", help="Realm to attempt logins at")
    parser.addoption("--randomly-seed", help="Seed to use for randomization.")


@pytest.fixture(scope="session")
def base_seed(pytestconfig) -> int:
    """
    Interim solution to randomize the integrated Faker.

    Long term we aim to go for ``pytest-randomly``.
    """
    base_seed = pytestconfig.getoption("--randomly-seed")
    if not base_seed:
        base_seed = random.randint(1000, 9999)
    print("base seed: ", base_seed)
    return base_seed


@pytest.fixture(scope="function", autouse=True)
def faker_seed(base_seed, request):
    """
    Generates unique but deterministic seeds for every test function.
    Based on a root seed and the test function name.

    When faker is used in a fixture that is used by multiple test functions.
    Each function expects different faker data.
    This is essential to avoid cross-contamination between tests
    because of test objects like LDAP users or groups.
    At the same time, the faker seed needs to stay deterministic.
    """
    test_function_name = request.node.name
    if hasattr(request, "param"):
        seed = f"{base_seed}-{test_function_name}-{request.param}"
    else:
        seed = f"{base_seed}-{test_function_name}"
    logger.info("Generated faker seed unique to the test function is: %s", seed)
    return seed


@pytest.fixture(scope="session")
def release_name():
    """
    Discovers the release name based on the env variable RELEASE_NAME.

    Will fallback to "nubus" if the variable is not set.
    """
    value = os.getenv("RELEASE_NAME", "nubus")
    return value


@pytest.fixture(scope="session")
def k8s():
    """
    Kubernetes abstraction.

    Returns a utility to interact with a Kubernetes cluster.
    """
    cluster = KubernetesCluster()
    yield cluster
    cluster.cleanup()


@pytest.fixture(scope="session")
def portal(pytestconfig, k8s, release_name):
    """
    Returns an instance of `PortalDeployment`.
    """
    cli_base_url = pytestconfig.getoption("--portal-base-url")
    return PortalDeployment(k8s, release_name, override_base_url=cli_base_url)


@pytest.fixture(scope="session")
def keycloak(pytestconfig, k8s, release_name):
    """
    Returns an instance of `PortalDeployment`.
    """
    cli_base_url = pytestconfig.getoption("--keycloak-base-url")
    return KeycloakDeployment(k8s, release_name, override_base_url=cli_base_url)


@pytest.fixture(scope="session")
def stack_data(k8s, release_name):
    """
    Returns an instance of `StackDataDeployment`.
    """
    return StackDataDeployment(k8s, release_name)


@pytest.fixture(scope="session")
def udm_rest_api(k8s, release_name):
    """
    Returns an instance of `UdmRestApiDeployment`.
    """
    return UdmRestApiDeployment(k8s, release_name)


@pytest.fixture(scope="session")
def ldap(k8s, release_name):
    """
    Returns an instance of `LdapDeployment`.
    """
    return LdapDeployment(k8s, release_name)
