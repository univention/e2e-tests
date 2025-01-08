# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import logging
import os
import time

from kubernetes import client, config
from kubernetes.client.rest import ApiException

from .port_forward import PortForwardingManager

log = logging.getLogger(__name__)


class KubernetesCluster:
    """
    Represents a Kubernetes Cluster and allows interaction via its API.

    The purpose of this fixture is to provide knowledge about and access into
    the Kubernetes cluster under test:

    - Help to bootstrap the access into the Kubernetes API.

    - Provide information about the selected default target namespace.

    - Utilities to help with common operations like waiting for a Pod status or
      inspecting the logs of a Pod or Container.

    - Potentially support to provide temporary namespaces and to apply
      Kubernetes Resources or Helm charts.

    The idea of this fixture is to support eventually two modes of operation:

    - "in-cluster" means that the code is running inside a Pod within the
      cluster under test. This mainly affects the configuration of the
      Kubernetes client and the way how Pods and Services are accessed.

      The configuration of the Kubernetes client will be done based on a
      ServiceAccount which has to have sufficient access rights and the token
      has to be mounted in the default locations.

    - "external" means that the code is not running inside the cluster under
      test.

      The configuration of the Kubernetes client will be based the default ways
      how also tools like `kubectl` are configured.

      Access to Pods and Services will by default have to be based on port
      forwarding. VPN'alike tooling may provide direct connection to Pods and
      Services, this is currently not used and support for this may have to be
      implemented when needed.
    """

    # The timeout values are tweaked to suite our development cluster.
    # Different target clusters may require adjustments.

    LDAP_READY_TIMEOUT = 120
    """Reasonable time to wait for an ldap pod to become available again."""

    POD_REMOVED_TIMEOUT = 5
    """Time to wait for a Pod to be removed when using a minimal grace period."""

    direct_access = False
    """Flag to indicate if direct access into the cluster resources is possible."""

    in_cluster = False
    """Flag to indicate if the code runs inside of the target cluster."""

    def __init__(self):
        config.load_kube_config()
        self.port_forwarding = PortForwardingManager()
        self.namespace = discover_namespace()
        if not self.direct_access:
            self.port_forwarding.start_monitoring()

    def port_forward_if_needed(
        self,
        target_name: str,
        target_port: int,
        local_port: int | None = None,
        target_type: str = "pod",
        target_namespace: str | None = None,
    ) -> tuple[str, int]:
        if self.direct_access:
            return target_name, target_port
        else:
            return self.port_forward(
                target_name,
                target_port,
                local_port,
                target_type,
                target_namespace,
            )

    def port_forward(
        self,
        target_name: str,
        target_port: int,
        local_port: int | None = None,
        target_type: str = "pod",
        target_namespace: str | None = None,
    ) -> tuple[str, int]:
        if target_namespace is None:
            target_namespace = self.namespace
        used_port = self.port_forwarding.add(
            target_namespace,
            target_name,
            target_port,
            local_port,
            target_type,
        )
        # TODO: Give kubectl a chance to have the socket ready. Better
        # would be a check if the Socket can be reached or similar.
        time.sleep(1)
        return "localhost", used_port

    def cleanup(self):
        self.port_forwarding.stop_monitoring()

    def delete_pod(self, pod_name: str, namespace: str | None = None):
        if not namespace:
            namespace = self.namespace
        api = client.CoreV1Api()
        print(f"Deleting pod {pod_name}...")
        api.delete_namespaced_pod(
            name=pod_name,
            namespace=namespace,
            body=client.V1DeleteOptions(grace_period_seconds=0, propagation_policy="Foreground"),
        )

    def delete_pod_pvc(self, pod_name: str, namespace: str | None = None):
        if not namespace:
            namespace = self.namespace
        api = client.CoreV1Api()
        print(f"Deleting pod {pod_name} and its PVCs...")
        try:
            pod = api.read_namespaced_pod(name=pod_name, namespace=namespace)
            pvc_names = []
            for volume in pod.spec.volumes:
                if volume.persistent_volume_claim:
                    pvc_name = volume.persistent_volume_claim.claim_name
                    pvc_names.append(pvc_name)
                    print(f"Found PVC to delete: {pvc_name}")

            for pvc_name in pvc_names:
                print(f"Deleting PVC {pvc_name}...")
                api.delete_namespaced_persistent_volume_claim(
                    name=pvc_name, namespace=namespace, body=client.V1DeleteOptions(propagation_policy="Foreground")
                )

            self.delete_pod(pod_name, namespace)
            print("Pod and PVCs deleted successfully")
        except ApiException as e:
            print(f"Error deleting pod or PVC: {e}")
            raise RuntimeError(f"Failed to delete pod or PVC: {e}")

    def check_pod_logs(
        self,
        pod_name: str,
        namespace: str | None = None,
        container_name: str | None = None,
        tail_lines: int | None = None,
    ):
        """
        Get pod logs.

        Args:
            api: Kubernetes API client
            pod_name: Name of the pod
            namespace: Kubernetes namespace
            container_name: Name of the container (optional)
            tail_lines: Number of lines to fetch from the end
        """
        if not namespace:
            namespace = self.namespace
        api = client.CoreV1Api()
        try:
            return api.read_namespaced_pod_log(
                name=pod_name, namespace=namespace, container=container_name, tail_lines=tail_lines
            )
        except ApiException as e:
            raise RuntimeError(f"Failed to get pod logs: {e}")

    def wait_for_pod_ready(self, pod_name: str, namespace: str | None = None, timeout: int = 300):
        if not namespace:
            namespace = self.namespace
        api = client.CoreV1Api()
        print(f"Waiting for pod {pod_name} to be ready (timeout: {timeout}s)...")
        start_time = time.time()
        while True:
            try:
                pod = api.read_namespaced_pod(name=pod_name, namespace=namespace)
                if pod.status.phase == "Running":
                    ready = True
                    for container_status in pod.status.container_statuses:
                        if not container_status.ready:
                            ready = False
                            break
                    if ready:
                        print(f"Pod {pod_name} is ready")
                        return True
            except ApiException as e:
                if e.status != 404:
                    raise
            if time.time() - start_time > timeout:
                raise TimeoutError(f"Pod {pod_name} did not become ready within {timeout} seconds")
            time.sleep(5)
            print(".", end="", flush=True)


def discover_namespace():
    _, active_context = config.list_kube_config_contexts()
    namespace_from_context = active_context["context"]["namespace"]
    namespace = os.environ.get("DEPLOY_NAMESPACE", namespace_from_context)
    log.info("Discovered target namespace: %s", namespace)
    return namespace
