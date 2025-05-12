# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import logging

from e2e.base import BaseDeployment
from e2e.kubernetes import KubernetesCluster

log = logging.getLogger(__name__)


class KeycloakDeployment(BaseDeployment):
    """
    Represents a deployment of Keycloak.
    """

    base_url: str = None
    """
    Base URL to reach Keycloak.

    Example: "https://id.domain.example/".
    """

    def __init__(self, k8s: KubernetesCluster, release_name: str, *, override_base_url: str | None = None):
        if override_base_url:
            self.base_url = override_base_url
            log.warning("Overriding keycloak base_url to %s", override_base_url)
        super().__init__(k8s, release_name)

    def _discover_from_cluster(self):
        if self.base_url:
            return
        url_parts = self._k8s.discover_url_parts_from_ingress(self.add_release_prefix("keycloak"))
        self.base_url = url_parts.to_url()
