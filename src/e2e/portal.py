# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from base64 import b64decode

from e2e.base import BaseDeployment
from e2e.kubernetes import KubernetesCluster
from e2e.kubernetes.utils import get_secret_by_volume


class PortalDeployment(BaseDeployment):
    """
    Represents a deployment of the portal.
    """

    service_account_username = "svc-portal-server"
    service_account_password = None

    def __init__(self, k8s: KubernetesCluster, release_name: str):
        super().__init__(k8s, release_name)

    def _discover_from_cluster(self):
        deployment_name = self.add_release_prefix("portal-server")
        deployment = self._k8s.get_deployment(deployment_name)
        secret_details = get_secret_by_volume(
            deployment.spec.template.spec, container_name="portal-server", volume_name="secret-udm"
        )

        secret = self._k8s.get_secret(secret_details.name)
        self.service_account_password = b64decode(secret.data[secret_details.key])
