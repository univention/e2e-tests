# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import logging

from e2e.kubernetes import KubernetesCluster

log = logging.getLogger(__name__)


class KeycloakDeployment:
    """
    Represents a deployment of Keycloak.
    """

    base_url: str = None
    """
    Base URL to reach Keycloak.

    Example: "https://id.domain.example/".
    """

    def __init__(self, k8s: KubernetesCluster, *, override_base_url: str | None = None):
        self._k8s = k8s

        if override_base_url:
            log.warning("Overriding discovered keycloak base_url from %s to %s", self.base_url, override_base_url)
            self.base_url = override_base_url
        else:
            url_parts = self._k8s.discover_url_parts_from_ingress(
                self._k8s.add_release_prefix("keycloak"),
            )
            self.base_url = url_parts.to_url()
