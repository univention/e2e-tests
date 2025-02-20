# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from e2e.base import BaseDeployment
from e2e.kubernetes import KubernetesCluster
from e2e.stack_data import StackDataDeployment


class PortalDeployment(BaseDeployment):
    """
    Represents a deployment of the portal.
    """

    service_account_username = "svc-portal-server"
    service_account_password = None

    # TODO: Remove "stack_data" again once the username and password are supplied to the
    # portal server directly.
    def __init__(self, k8s: KubernetesCluster, release_name: str, stack_data: StackDataDeployment):
        self._stack_data = stack_data
        super().__init__(k8s, release_name)

    def _discover_from_cluster(self):
        self.service_account_password = self._stack_data.template_context["svcPortalServerUserPassword"]
