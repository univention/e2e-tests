# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import logging
import os
import time

from kubernetes import config

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


def discover_namespace():
    _, active_context = config.list_kube_config_contexts()
    namespace_from_context = active_context["context"]["namespace"]
    namespace = os.environ.get("DEPLOY_NAMESPACE", namespace_from_context)
    log.info("Discovered target namespace: %s", namespace)
    return namespace
