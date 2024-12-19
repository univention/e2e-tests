# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import os

from kubernetes import client, config
from kubernetes.client import ApiClient
from kubernetes.dynamic import DynamicClient
import ldap3
import ldap3.core.exceptions
import pytest

from e2e.chaos import ChaosMeshFixture
from e2e.ldap import LDAPFixture
from e2e.kubernetes import KubernetesCluster

from env_vars import EnvConfig
from utils.k8s_helpers import wait_for_pod_ready


@pytest.fixture(scope="session")
def k8s():
    """
    Kubernetes abstraction.

    Returns a utility to interact with a Kubernetes cluster.
    """
    cluster = KubernetesCluster()
    yield cluster
    cluster.cleanup()


@pytest.fixture(autouse=True, scope="session")
def k8s_configure_client():
    """
    Configures the Kubernetes client.

    Does not (yet) support in-cluster configuration.
    """
    config.load_kube_config()


@pytest.fixture(scope="session")
def env(k8s, release_name):
    """Provide an instance of EnvConfig."""
    return EnvConfig(k8s.namespace, release_name)


@pytest.fixture(scope="session")
def k8s_api(env):
    """Initialize and return Kubernetes API client."""
    return env.k8s_api


@pytest.fixture(scope="session")
def k8s_apps_api():
    """Initialize and return Kubernetes Apps API client."""
    config.load_kube_config()
    return client.AppsV1Api()


@pytest.fixture
def k8s_chaos(k8s):
    """
    Returns a configured `ChaosMeshFixture` instance.

    This allows to deploy various chaos experiment types from Chaos Mesh. It will
    clean up the Kubernetes resources at the end of the test case.
    """
    client = DynamicClient(ApiClient())
    chaos_mesh = ChaosMeshFixture(client, k8s.namespace)
    yield chaos_mesh
    chaos_mesh.cleanup()


def create_ldap_connection(k8s, pod_name: str, local_port: int, env):
    """Create a new LDAP connection with port forwarding."""
    try:
        pod_port = 389
        hostname, port = k8s.port_forward_if_needed(pod_name, pod_port, local_port)
        uri = f"ldap://{hostname}:{port}"
        server = ldap3.Server(host=uri, connect_timeout=5)
        conn = ldap3.Connection(
            server,
            user=env.LDAP_ADMIN_DN,
            password=env.LDAP_ADMIN_PASSWORD,
            raise_exceptions=True,
            client_strategy="RESTARTABLE",
        )
        conn.bind()
        return conn
    except Exception as e:
        print(f"Failed to set up LDAP connection: {e}")
        raise


@pytest.fixture
def ldap_primary_0(k8s, k8s_api, env):
    """Return a factory function for getting connections to first LDAP primary."""
    pod_name = f"{env.release_prefix}ldap-server-primary-0"
    local_port = 3890

    def get_connection():
        wait_for_pod_ready(k8s_api, pod_name, k8s.namespace)
        return create_ldap_connection(k8s, pod_name, local_port, env)

    return get_connection


@pytest.fixture
def ldap_primary_1(k8s, k8s_api, env):
    """Return a factory function for getting connections to second LDAP primary."""
    pod_name = f"{env.release_prefix}ldap-server-primary-1"
    local_port = 3891

    def get_connection():
        wait_for_pod_ready(k8s_api, pod_name, k8s.namespace)
        return create_ldap_connection(k8s, pod_name, local_port, env)

    return get_connection


@pytest.fixture
def cleanup_ldap(ldap_primary_0, env):
    """Cleanup LDAP data after tests."""
    yield
    base_dn = env.LDAP_BASE_DN
    conn_primary_0 = ldap_primary_0()

    # Delete test users
    print("Deleting test users")
    user_filter = "(uid=test-user-*)"
    conn_primary_0.search(f"cn=users,{base_dn}", user_filter, ldap3.LEVEL)
    for item in conn_primary_0.response:
        try:
            conn_primary_0.delete(item["dn"])
        except ldap3.core.exceptions.LDAPException:
            pass

    # Delete test groups
    print("Deleting test groups")
    group_filter = "(cn=test-group-*)"
    conn_primary_0.search(f"cn=groups,{base_dn}", group_filter, ldap3.LEVEL)
    for item in conn_primary_0.response:
        try:
            conn_primary_0.delete(item["dn"])
        except ldap3.core.exceptions.LDAPException:
            pass

    # Delete dummy user if it exists
    try:
        print("Deleting dummy user")
        conn_primary_0.delete(f"cn=dummy,cn=users,{base_dn}")
    except ldap3.core.exceptions.LDAPException:
        pass

    print("Finished cleanup")


@pytest.fixture(scope="session")
def release_name():
    """
    Discovers the release name based on the env variable RELEASE_NAME.

    Will fallback to "nubus" if the variable is not set.
    """
    value = os.getenv("RELEASE_NAME", "nubus")
    return value


@pytest.fixture
def ldap(k8s, release_name):
    """
    Returns an instance of `LDAPFixture`.
    """
    return LDAPFixture(k8s, release_name)
