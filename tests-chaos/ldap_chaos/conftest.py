# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import os

import pytest
from kubernetes import config


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
