# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import logging
from base64 import b64decode
from urllib.parse import urljoin

from kubernetes.client import models

from e2e.base import BaseDeployment
from e2e.kubernetes import KubernetesCluster
from e2e.kubernetes.utils import get_secret_by_volume

log = logging.getLogger(__name__)


class PortalDeployment(BaseDeployment):
    """
    Represents a deployment of the portal.
    """

    base_url: str | None = None
    """
    Base URL to reach the Portal deployment.

    This does not include a prefix like `/univention/portal/`.

    Example: "https://domain.example/".
    """

    service_account_username = "svc-portal-server"
    service_account_password = None

    central_navigation_shared_secret = None

    def __init__(self, k8s: KubernetesCluster, release_name: str, *, override_base_url: str | None = None):
        if override_base_url:
            log.warning("Overriding portal base_url to %s", override_base_url)
            self.base_url = override_base_url
        super().__init__(k8s, release_name)

    def _discover_from_cluster(self):
        deployment_name = self.add_release_prefix("portal-server")
        deployment = self._k8s.get_deployment(deployment_name)

        self.service_account_password = self._discover_secret_value_from_volume(
            deployment.spec.template.spec,
            container_name="portal-server",
            volume_name="secret-udm",
        )
        self.central_navigation_shared_secret = self._discover_secret_value_from_volume(
            deployment.spec.template.spec,
            container_name="portal-server",
            volume_name="secret-central-navigation",
        )

        if not self.base_url:
            url_parts = self._k8s.discover_url_parts_from_ingress(
                self.add_release_prefix("portal-frontend-rewrites"),
                self._k8s.namespace,
            )
            self.base_url = url_parts.to_url()

    def _discover_secret_value_from_volume(
        self,
        pod_spec: models.V1PodSpec,
        container_name: str,
        volume_name: str,
    ) -> str:
        secret_details = get_secret_by_volume(
            pod_spec, container_name=container_name, volume_name=volume_name,
        )
        secret = self._k8s.get_secret(secret_details.name)
        return b64decode(secret.data[secret_details.key])

    @property
    def favicon_well_known_url(self):
        return urljoin(self.base_url, "/favicon.ico")

    @property
    def central_navigation_url(self):
        return urljoin(self.base_url, "/univention/portal/navigation.json")
