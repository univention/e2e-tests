# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import time

from e2e.base import BaseDeployment
from e2e.kubernetes import KubernetesCluster


class UniventionManagementConsoleDeployment(BaseDeployment):
    """
    Represents a deployment of the Univention Management Console (UMC).
    """

    def __init__(self, k8s: KubernetesCluster, release_name: str):
        """Initializes the UMC deployment object."""
        super().__init__(k8s, release_name)
        self.umc_server_stateful_set_name = self.add_release_prefix("umc-server")
        self.memcached_deployment_name = self.add_release_prefix("umc-server-memcached")

    def restart_umc(self):
        """Restarts the UMC server and memcached, and waits for them to be ready."""
        umc_pod_names = self._k8s.get_pod_names_for_stateful_set(self.umc_server_stateful_set_name)

        for pod_name in umc_pod_names:
            self._k8s.delete_pod(pod_name)

        self.wait_for_umc()

    def restart_memcached(self):
        """Restarts the memcached pods and waits for them to be ready."""
        memcached_pod_names = self._k8s.get_pod_names_for_deployment(self.memcached_deployment_name)

        for pod_name in memcached_pod_names:
            self._k8s.delete_pod(pod_name)

        self.wait_for_memcached()

        # when the container switches to "ready" memcached is not immediately ready to accept connections
        time.sleep(3)

    def wait_for_memcached(self):
        """Waits for all memcached pods to be running and ready."""
        memcached_pod_names = []
        pods_wanted = self._k8s.get_deployment(self.memcached_deployment_name).spec.replicas
        while len(memcached_pod_names) != pods_wanted:
            memcached_pod_names = self._k8s.get_pod_names_for_deployment(self.memcached_deployment_name)

        for pod in memcached_pod_names:
            self._k8s.wait_for_pod_ready(pod)

    def wait_for_umc(self):
        """Waits for all UMC server pods to be running and ready."""
        umc_pod_names = []
        pods_wanted = self._k8s.get_stateful_set(self.umc_server_stateful_set_name).spec.replicas
        while len(umc_pod_names) != pods_wanted:
            umc_pod_names = self._k8s.get_pod_names_for_stateful_set(self.umc_server_stateful_set_name)

        for pod in umc_pod_names:
            self._k8s.wait_for_pod_ready(pod)
