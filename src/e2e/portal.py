# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from base64 import b64decode

import yaml
from kubernetes import client

from e2e.helm import add_release_prefix
from e2e.kubernetes import KubernetesCluster


class PortalDeployment:
    """
    Represents a deployment of the portal.
    """

    service_account_username = "svc-portal-server"
    service_account_password = None

    def __init__(self, k8s: KubernetesCluster, release_name: str):
        self._k8s = k8s
        self.release_name = release_name
        self._discover_from_cluster()

    def _discover_from_cluster(self):
        # TODO: It seems that a "Portal Deployment" does depend on a "StackDataDeployment".
        # Avoid hardcoding the stack-data internals here.
        template_context_name = add_release_prefix("stack-data-ums-context", self.release_name)
        v1 = client.CoreV1Api()

        secret = v1.read_namespaced_secret(
            name=template_context_name,
            namespace=self._k8s.namespace,
        )
        template_context_yaml = b64decode(secret.data["context.yaml"]).decode()
        template_context = yaml.safe_load(template_context_yaml)
        self.service_account_password = template_context["svcPortalServerUserPassword"]
