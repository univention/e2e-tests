# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

# conftest.py
import subprocess
import os
from typing import Dict

import ldap as pyldap
import pytest
from env_vars import EnvConfig
from kubernetes import client, config
from kubernetes.client import ApiClient
from kubernetes.dynamic import DynamicClient
from utils.k8s_helpers import setup_port_forward, wait_for_pod_ready



from e2e.chaos import ChaosMeshFixture
from e2e.ldap import LDAPFixture

@pytest.fixture(autouse=True, scope="session")
def k8s_configure_client():
    """
    Configures the Kubernetes client.

    Does not (yet) support in-cluster configuration.
    """
    config.load_kube_config()


@pytest.fixture(scope="session")
def env():
    """Provide an instance of EnvConfig."""
    return EnvConfig()


@pytest.fixture(scope="session")
def k8s_namespace():
    """
    The Kubernetes Namespace to use when interacting with the cluster.

    The namespace is selected from the currently active context. Inspect and
    prepare via ``kubens``.
    """
    _, active_context = config.list_kube_config_contexts()
    namespace_from_context = active_context["context"]["namespace"]
    namespace = os.environ.get("DEPLOY_NAMESPACE", namespace_from_context)
    print("namespace:", namespace)
    return namespace


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
def k8s_chaos(k8s_namespace):
    """
    Returns a configured `ChaosMeshFixture` instance.

    This allows to deploy various chaos experiment types from Chaos Mesh. It will
    clean up the Kubernetes resources at the end of the test case.
    """
    client = DynamicClient(ApiClient())
    chaos_mesh = ChaosMeshFixture(client, k8s_namespace)
    yield chaos_mesh
    chaos_mesh.cleanup()


@pytest.fixture(scope="session")
def port_forwarder(env):
    """Manage kubectl port-forward processes."""
    processes: Dict[str, subprocess.Popen] = {}

    def forward_port(pod_name: str, local_port: int):
        if pod_name in processes:
            processes[pod_name].terminate()
        process = setup_port_forward(pod_name, env.k8s_namespace, local_port)
        processes[pod_name] = process

    yield forward_port

    # Cleanup
    for process in processes.values():
        process.terminate()


def create_ldap_connection(pod_name: str, local_port: int, port_forwarder, env):
    """Create a new LDAP connection with port forwarding."""
    try:
        port_forwarder(pod_name, local_port)
        uri = f"ldap://localhost:{local_port}"
        conn = pyldap.initialize(uri)
        conn.simple_bind_s(env.LDAP_ADMIN_DN, env.LDAP_ADMIN_PASSWORD)
        return conn
    except Exception as e:
        print(f"Failed to set up LDAP connection: {e}")
        raise


@pytest.fixture
def ldap_primary_0(k8s_api, port_forwarder, env):
    """Return a factory function for getting connections to first LDAP primary."""
    pod_name = f"{env.release_prefix}ldap-server-primary-0"
    local_port = 3890

    def get_connection():
        wait_for_pod_ready(k8s_api, pod_name, env.k8s_namespace)
        return create_ldap_connection(pod_name, local_port, port_forwarder, env)

    return get_connection


@pytest.fixture
def ldap_primary_1(k8s_api, port_forwarder, env):
    """Return a factory function for getting connections to second LDAP primary."""
    pod_name = f"{env.release_prefix}ldap-server-primary-1"
    local_port = 3891

    def get_connection():
        wait_for_pod_ready(k8s_api, pod_name, env.k8s_namespace)
        return create_ldap_connection(pod_name, local_port, port_forwarder, env)

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
    results = conn_primary_0.search_s(f"cn=users,{base_dn}", pyldap.SCOPE_ONELEVEL, user_filter)
    for dn, _ in results:
        try:
            conn_primary_0.delete_s(dn)
        except pyldap.LDAPError:
            pass

    # Delete test groups
    print("Deleting test groups")
    group_filter = "(cn=test-group-*)"
    results = conn_primary_0.search_s(f"cn=groups,{base_dn}", pyldap.SCOPE_ONELEVEL, group_filter)
    for dn, _ in results:
        try:
            conn_primary_0.delete_s(dn)
        except pyldap.LDAPError:
            pass

    # Delete dummy user if it exists
    try:
        print("Deleting dummy user")
        conn_primary_0.delete_s(f"cn=dummy,cn=users,{base_dn}")
    except pyldap.LDAPError:
        pass

    print("Finished cleanup")


@pytest.fixture
def ldap():
    """
    Returns an instance of `LDAPFixture`.
    """
    return LDAPFixture()
