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
        ingress_name = self.add_release_prefix("udm-rest-api")
        ingress = self._k8s.get_ingress(ingress_name)
        host = ingress.spec.rules[0].host
        tls = ingress.spec.tls
        scheme = "https" if tls else "http"
        port = self._k8s.ingress_https_port if tls else self._k8s.ingress_http_port
        self.base_url = f"{scheme}://{host}:{port}/univention/udm/"
