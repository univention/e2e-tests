# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

# conftest.py
import subprocess
from typing import Dict

import ldap
import pytest
from env_vars import env
from kubernetes import client, config
from utils.k8s_helpers import setup_port_forward, wait_for_pod_ready


@pytest.fixture(scope="session")
def k8s_api():
    """Initialize and return Kubernetes API client."""
    return env.k8s_api


@pytest.fixture(scope="session")
def k8s_apps_api():
    """Initialize and return Kubernetes Apps API client."""
    config.load_kube_config()
    return client.AppsV1Api()


@pytest.fixture(scope="session")
def port_forwarder():
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


def create_ldap_connection(pod_name: str, local_port: int, port_forwarder):
    """Create a new LDAP connection with port forwarding."""
    try:
        port_forwarder(pod_name, local_port)
        uri = f"ldap://localhost:{local_port}"
        conn = ldap.initialize(uri)
        conn.simple_bind_s(env.LDAP_ADMIN_DN, env.LDAP_ADMIN_PASSWORD)
        return conn
    except Exception as e:
        print(f"Failed to set up LDAP connection: {e}")
        raise


@pytest.fixture
def ldap_primary_0(k8s_api, port_forwarder):
    """Return a factory function for getting connections to first LDAP primary."""
    pod_name = f"{env.HELM_RELEASE_NAME}-ldap-server-primary-0"
    local_port = 3890

    def get_connection():
        wait_for_pod_ready(k8s_api, pod_name, env.k8s_namespace)
        return create_ldap_connection(pod_name, local_port, port_forwarder)

    return get_connection


@pytest.fixture
def ldap_primary_1(k8s_api, port_forwarder):
    """Return a factory function for getting connections to second LDAP primary."""
    pod_name = f"{env.HELM_RELEASE_NAME}-ldap-server-primary-1"
    local_port = 3891

    def get_connection():
        wait_for_pod_ready(k8s_api, pod_name, env.k8s_namespace)
        return create_ldap_connection(pod_name, local_port, port_forwarder)

    return get_connection


@pytest.fixture
def cleanup_ldap(ldap_primary_0):
    """Cleanup LDAP data after tests."""
    yield
    base_dn = env.LDAP_BASE_DN
    conn_primary_0 = ldap_primary_0()

    # Delete test users
    print("Deleting test users")
    user_filter = "(uid=test-user-*)"
    results = conn_primary_0.search_s(f"cn=users,{base_dn}", ldap.SCOPE_ONELEVEL, user_filter)
    for dn, _ in results:
        try:
            conn_primary_0.delete_s(dn)
        except ldap.LDAPError:
            pass

    # Delete test groups
    print("Deleting test groups")
    group_filter = "(cn=test-group-*)"
    results = conn_primary_0.search_s(f"cn=groups,{base_dn}", ldap.SCOPE_ONELEVEL, group_filter)
    for dn, _ in results:
        try:
            conn_primary_0.delete_s(dn)
        except ldap.LDAPError:
            pass

    # Delete dummy user if it exists
    try:
        print("Deleting dummy user")
        conn_primary_0.delete_s(f"cn=dummy,cn=users,{base_dn}")
    except ldap.LDAPError:
        pass

    print("Finished cleanup")
