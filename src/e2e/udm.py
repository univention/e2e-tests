# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import logging
from urllib.parse import urljoin

from e2e.kubernetes import KubernetesCluster

log = logging.getLogger(__name__)


class UdmRestApiDeployment:
    """
    Represents a deployment of the UDM Rest API.
    """

    base_url: str | None = None
    """
    Base URL to reach the UDM Rest API deployment.

    Example: "https://domain.example/univention/portal/udm/".
    """

    def __init__(self, k8s: KubernetesCluster, override_base_url: str | None = None):
        self._k8s = k8s

        if override_base_url:
            log.warning("Overriding udm base_url to %s", override_base_url)
            self.base_url = override_base_url
        else:
            url_parts = self._k8s.discover_url_parts_from_ingress(
                self._k8s.add_release_prefix("udm-rest-api"),
            )
            self.base_url = urljoin(url_parts.to_url(), "/univention/udm/")
