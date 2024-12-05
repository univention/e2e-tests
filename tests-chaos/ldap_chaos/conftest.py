# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import os

import pytest
from kubernetes import config
from kubernetes.client import ApiClient
from kubernetes.dynamic import DynamicClient

from e2e.chaos import ChaosMeshFixture


@pytest.fixture(autouse=True, scope="session")
def k8s_configure_client():
    """
    Configures the Kubernetes client.

    Does not (yet) support in-cluster configuration.
    """
    config.load_kube_config()


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
