import logging
import os
import signal
import subprocess
import time


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
        self.port_forward_processes: dict[str, subprocess.Popen] = {}

    def port_forward_if_needed(
        self,
        target_name: str,
        target_namespace: str,
        target_port: int,
        local_port: int,
        target_type: str = "pod"
    ) -> tuple[str, int]:
        if self.direct_access:
            return target_name, target_port

        if target_name in self.port_forward_processes:
            self._terminate_forward_process(target_name, self.port_forward_processes[target_name])
        process = setup_port_forward(
            target_name,
            target_namespace,
            local_port,
            target_type=target_type,
        )
        self.port_forward_processes[f"{target_type}/{target_name}"] = process
        return "localhost", local_port

    def cleanup(self):
        self._cleanup_port_forward_processes()

    def _cleanup_port_forward_processes(self):
        for name, process in self.port_forward_processes.items():
            self._terminate_forward_process(name, process)

    def _terminate_forward_process(self, name, process):
        log.debug("Terminating port forwarding subprocess %s", name)
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        os.killpg(os.getpgid(process.pid), signal.SIGKILL)
        process.terminate()
        process.kill()
        process.wait(timeout=5)





def setup_port_forward(
    target_name: str,
    namespace: str,
    local_port: int,
    remote_port: int = 389,
    target_type: str = "pod",
):
    """
    Setup kubectl port-forward and return the process.
    """
    cmd = [
        "kubectl",
        "port-forward",
        f"{target_type}/{target_name}",
        f"{local_port}:{remote_port}",
        "-n", namespace,
    ]
    cmd = "while true; do " + " ".join(cmd) + "; sleep 1; done"
    log.debug("Calling kubectl: %s", cmd)
    process = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
    # Give it some time to establish the connection
    time.sleep(2)
    return process
