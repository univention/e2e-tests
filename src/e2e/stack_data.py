# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from base64 import b64decode

import yaml
from kubernetes import client

from e2e.helm import add_release_prefix
from e2e.kubernetes import KubernetesCluster


class StackDataDeployment:
    """
    Represents a deployment of stack-data.
    """

    template_context_secret_base_name = "stack-data-ums-context"
    template_context_file_name = "context.yaml"

    def __init__(self, k8s: KubernetesCluster, release_name: str):
        self._k8s = k8s
        self.release_name = release_name
        self._discover_from_cluster()

    def _discover_from_cluster(self):
        template_context_name = add_release_prefix(self.template_context_secret_base_name, self.release_name)
        v1 = client.CoreV1Api()

        secret = v1.read_namespaced_secret(
            name=template_context_name,
            namespace=self._k8s.namespace,
        )
        template_context_yaml = b64decode(secret.data[self.template_context_file_name]).decode()
        self.template_context = yaml.safe_load(template_context_yaml)
