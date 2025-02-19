# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import pytest
from kubernetes.client import ApiClient
from kubernetes.dynamic import DynamicClient

from e2e.chaos import ChaosMeshFixture
from e2e.ldap import LdapDeployment


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


@pytest.fixture
def ldap(k8s, release_name):
    """
    Returns an instance of `LdapDeployment`.
    """
    return LdapDeployment(k8s, release_name)
