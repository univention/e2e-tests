# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH


import logging
from urllib.parse import urljoin

from e2e.base import BaseDeployment
from e2e.kubernetes import KubernetesCluster

log = logging.getLogger(__name__)


class UdmRestApiDeployment(BaseDeployment):
    """
    Represents a deployment of the UDM Rest API.
    """

    base_url: str = None
    """
    Base URL to reach the UDM Rest API deployment.

    Example: "https://domain.example/univention/portal/udm/".
    """

    def __init__(self, k8s: KubernetesCluster, release_name: str, *, override_base_url: str = None):
        super().__init__(k8s, release_name)
        if override_base_url:
            override_base_url = _add_udm_subpath(override_base_url)
            log.warning(
                "Overriding discovered UDM Rest API base_url from %s to %s",
                self.base_url,
                override_base_url,
            )
            self.base_url = override_base_url

    def _discover_from_cluster(self):
        url_parts = self._k8s.discover_url_parts_from_ingress(
            self.add_release_prefix("udm-rest-api"),
        )
        self.base_url = _add_udm_subpath(url_parts.to_url())


def _add_udm_subpath(url):
    return urljoin(url, "/univention/udm/")
