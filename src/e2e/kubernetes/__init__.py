# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import logging
import time
from typing import Any

from kubernetes import client, config
from kubernetes.client.models import V1Deployment
from kubernetes.client.rest import ApiException

from .port_forward import PortForwardingManager
from .utils import UrlParts

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

    direct_access = True
    """
    Flag to indicate if direct access into the cluster resources is possible.

    Automatic port forwarding will be enabled if this is set to `False`.
    """

    in_cluster = False
    """Flag to indicate if the code runs inside of the target cluster."""

    ingress_http_port = 80
    """The port for plain HTTP access of the ingress controller."""

    ingress_https_port = 443
    """The port for HTTPS access of the intress controller."""

    def __init__(
        self,
        override_namespace: str | None = None,
        direct_access=True,
    ):
        self.direct_access = direct_access
        config.load_kube_config()
        self.port_forwarding = PortForwardingManager()
        self.namespace = override_namespace or discover_namespace()
        self._discover_from_cluster()
        if not self.direct_access:
            self.port_forwarding.start_monitoring()

    def _discover_from_cluster(self):
        core_api = client.CoreV1Api()
        namespace = core_api.read_namespace(name=self.namespace)
        annotations = namespace.metadata.annotations
        if annotations:
            ingress_http_port = annotations.get("nubus.univention.dev/ingress-http-port")
            if ingress_http_port:
                log.info("Ingress http port discovered via annotation to be %s.", ingress_http_port)
                self.ingress_http_port = int(ingress_http_port)
            ingress_https_port = annotations.get("nubus.univention.dev/ingress-https-port")
            if ingress_https_port:
                log.info("Ingress https port discovered via annotation to be %s.", ingress_https_port)
                self.ingress_https_port = int(ingress_https_port)

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

    def scale_stateful_set(self, stateful_set_name: str, replicas: int, namespace: str | None = None):
        if not namespace:
            namespace = self.namespace
        api = client.AppsV1Api()
        print(f"Scaling StatefulSet {stateful_set_name} to {replicas} replicas ...")
        patch_replicas = [
            {
                "op": "replace",
                "path": "/spec/replicas",
                "value": replicas,
            }
        ]
        api.patch_namespaced_stateful_set(
            name=stateful_set_name,
            namespace=namespace,
            body=patch_replicas,
        )

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

    def get_deployment(self, name: str, namespace: str | None = None) -> V1Deployment:
        """
        Retrieve a `Deployment` from the cluster.

        If `namespace` is not provided, then the discovered namespace will be
        used.
        """
        v1 = client.AppsV1Api()
        deployment = v1.read_namespaced_deployment(
            name=name,
            namespace=namespace or self.namespace,
        )
        return deployment

    def get_ingress(self, name: str, namespace: str | None = None):
        """
        Retrieve an `Ingress` from the cluster.

        If `namespace` is not provided, then the discovered namespace will be
        used.
        """
        v1 = client.NetworkingV1Api()
        ingress = v1.read_namespaced_ingress(
            name=name,
            namespace=namespace or self.namespace,
        )
        return ingress

    def discover_url_parts_from_ingress(self, name: str, namespace: str | None = None):
        """
        Retrieve URL parts from an Ingress in the cluster.

        If `namespace` is not provided, then the discovered namespace will be
        used.
        """
        ingress = self.get_ingress(name, namespace or self.namespace)
        host = ingress.spec.rules[0].host
        tls = ingress.spec.tls
        scheme = "https" if tls else "http"
        port = self.ingress_https_port if tls else self.ingress_http_port
        return UrlParts(host=host, port=port, scheme=scheme)

    def get_secret(self, name: str, namespace: str | None = None):
        """
        Retrieve a `Secret` from the cluster.

        If `namespace` is not provided, then the discovered namespace will be
        used.
        """
        v1 = client.CoreV1Api()
        secret = v1.read_namespaced_secret(
            name=name,
            namespace=namespace or self.namespace,
        )
        return secret

    def get_configmap(self, name: str, namespace: str | None = None):
        """
        Retrieve a `Secret` from the cluster.

        If `namespace` is not provided, then the discovered namespace will be
        used.
        """
        v1 = client.CoreV1Api()
        configmap = v1.read_namespaced_config_map(name=name, namespace=namespace or self.namespace)

        return configmap

    def update_configmap_data(self, data_key: str, data_value: str, name: str, namespace: str | None = None):
        """
        Update a specific key-value pair in a `ConfigMap`.

        If `namespace` is not provided, then the discovered namespace will be
        used.
        """
        v1 = client.CoreV1Api()
        patch_configmap = [{"op": "replace", "path": f"/data/{data_key}", "value": data_value}]
        v1.patch_namespaced_config_map(name=name, namespace=namespace or self.namespace, body=patch_configmap)

    def get_stateful_set(self, name: str, namespace: str | None = None):
        """
        Retrieve a `StatefulSet` from the cluster.

        If `namespace` is not provided, then the discovered namespace will be
        used.
        """
        v1 = client.AppsV1Api()

        return v1.read_namespaced_stateful_set(name=name, namespace=namespace or self.namespace)

    def _get_pods_from_match_labels(self, labels: dict[str, Any], namespace: str | None = None):
        """
        Retrieve a list of `Pods` from the cluster that match the given labels.

        If `namespace` is not provided, then the discovered namespace will be
        used.
        """
        v1 = client.CoreV1Api()
        label_selector = ",".join([f"{k}={v}" for k, v in labels.items()])

        return v1.list_namespaced_pod(namespace=namespace or self.namespace, label_selector=label_selector)

    def get_pods_for_stateful_set(self, name: str, namespace: str | None = None):
        """
        Retrieve the `Pods` associated with a `StatefulSet`.

        If `namespace` is not provided, then the discovered namespace will be
        used.
        """
        stateful_set = self.get_stateful_set(name=name, namespace=namespace)

        return self._get_pods_from_match_labels(stateful_set.spec.selector.match_labels)

    def get_pod_names_for_stateful_set(self, name: str, namespace: str | None = None) -> list[str]:
        """
        Retrieve the names of the `Pods` associated with a `StatefulSet`.

        If `namespace` is not provided, then the discovered namespace will be
        used.
        """
        pods = self.get_pods_for_stateful_set(name=name, namespace=namespace)
        return [pod.metadata.name for pod in pods.items]

    def get_pods_for_deployment(self, name: str, namespace: str | None = None):
        """
        Retrieve the `Pods` associated with a `Deployment`.

        If `namespace` is not provided, then the discovered namespace will be
        used.
        """
        deployment = self.get_deployment(name=name, namespace=namespace)
        return self._get_pods_from_match_labels(deployment.spec.selector.match_labels, namespace)

    def get_pod_names_for_deployment(self, name: str, namespace: str | None = None) -> list[str]:
        """
        Retrieve the names of the `Pods` associated with a `Deployment`.

        If `namespace` is not provided, then the discovered namespace will be
        used.
        """
        pods = self.get_pods_for_deployment(name=name, namespace=namespace)
        return [pod.metadata.name for pod in pods.items]


def discover_namespace() -> str:
    _, active_context = config.list_kube_config_contexts()
    namespace = active_context["context"].get("namespace", "default")
    log.info("Discovered target namespace: %s", namespace)
    return namespace
