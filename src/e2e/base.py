# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from e2e.helm import add_release_prefix
from e2e.kubernetes import KubernetesCluster


class BaseDeployment:
    """
    Base class for deployment abstractions.
    """

    def __init__(self, k8s: KubernetesCluster):
        self._k8s = k8s
        self._discover_from_cluster()

    def _discover_from_cluster(self):
        """
        Discover configuration and secrets from cluster.

        This shall be implemented in sub classes.
        """

    def add_release_prefix(self, name: str) -> str:
        return add_release_prefix(name, self._k8s.release_name)
