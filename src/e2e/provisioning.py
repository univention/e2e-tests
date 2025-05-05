# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH


from base64 import b64decode

from e2e.kubernetes import KubernetesCluster


class ProvisioningApi:
    """
    Represents a deployment of the Provisioning API.
    """

    service_port = 80

    def __init__(self, k8s: KubernetesCluster):
        self._k8s = k8s

        self.service_name = self._k8s.add_release_prefix("provisioning-api")

        secret_name = self._k8s.add_release_prefix("provisioning-api-credentials")
        secret = self._k8s.get_secret(secret_name)
        self.admin_username = b64decode(secret.data["ADMIN_USERNAME"]).decode()
        self.admin_password = b64decode(secret.data["ADMIN_PASSWORD"]).decode()
