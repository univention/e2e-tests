# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH


from e2e.base import BaseDeployment
from e2e.kubernetes import KubernetesCluster


class UdmRestApiDeployment(BaseDeployment):
    """
    Represents a deployment of the UDM Rest API.
    """

    base_url: str = None
    """
    Base URL to reach the UDM Rest API deployment.

    Example: "https://domain.example/univention/portal/udm/".
    """

    def __init__(self, k8s: KubernetesCluster, release_name: str):
        super().__init__(k8s, release_name)

    def _discover_from_cluster(self):
        url_parts = self._k8s.discover_url_parts_from_ingress(
            self.add_release_prefix("udm-rest-api"),
        )
        self.base_url = f"{url_parts.scheme}://{url_parts.host}:{url_parts.port}/univention/udm/"
