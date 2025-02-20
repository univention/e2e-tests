# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH


from base64 import b64decode

from e2e.base import BaseDeployment
from e2e.kubernetes import KubernetesCluster


class ProvisioningApi(BaseDeployment):
    """
    Represents a deployment of the Provisioning API.
    """

    service_port = 80

    def __init__(self, k8s: KubernetesCluster, release_name: str):
        self.service_name = self.add_release_prefix("provisioning-api")
        super().__init__(k8s, release_name)

    def _discover_from_cluster(self):
        secret_name = self.add_release_prefix("provisioning-api-credentials")
        secret = self._k8s.get_secret(secret_name)

        self.admin_username = b64decode(secret.data["ADMIN_USERNAME"]).decode()
        self.admin_password = b64decode(secret.data["ADMIN_PASSWORD"]).decode()
