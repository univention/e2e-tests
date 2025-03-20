# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from e2e.base import BaseDeployment


class KeycloakDeployment(BaseDeployment):
    """
    Represents a deployment of Keycloak.
    """

    base_url: str = None
    """
    Base URL to reach Keycloak.

    Example: "https://id.domain.example/".
    """

    def _discover_from_cluster(self):
        ingress_name = self.add_release_prefix("keycloak")
        ingress = self._k8s.get_ingress(ingress_name)
        host = ingress.spec.rules[0].host
        tls = ingress.spec.tls
        scheme = "https" if tls else "http"
        port = self._k8s.ingress_https_port if tls else self._k8s.ingress_http_port
        self.base_url = f"{scheme}://{host}:{port}/"
