# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import os

import pytest
from kubernetes.client import ApiClient
from kubernetes.dynamic import DynamicClient

from e2e.chaos import ChaosMeshFixture
from e2e.kubernetes import KubernetesCluster
from e2e.ldap import LdapDeployment


@pytest.fixture(scope="session")
def k8s():
    """
    Kubernetes abstraction.

    Returns a utility to interact with a Kubernetes cluster.
    """
    cluster = KubernetesCluster()
    yield cluster
    cluster.cleanup()


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
    Returns an instance of `LdapDeployment`.
    """
    return LdapDeployment(k8s, release_name)
