# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import time

from kubernetes import client
from kubernetes.client.rest import ApiException


def wait_for_pod_ready(api: client.CoreV1Api, pod_name: str, namespace: str, timeout: int = 300):
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


def delete_pod(api: client.CoreV1Api, pod_name: str, namespace: str):
    print(f"Deleting pod {pod_name}...")
    api.delete_namespaced_pod(
        name=pod_name,
        namespace=namespace,
        body=client.V1DeleteOptions(grace_period_seconds=0, propagation_policy="Foreground"),
    )


def delete_pod_pvc(api: client.CoreV1Api, pod_name: str, namespace: str):
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

        delete_pod(api, pod_name, namespace)
        print("Pod and PVCs deleted successfully")
    except ApiException as e:
        print(f"Error deleting pod or PVC: {e}")
        raise RuntimeError(f"Failed to delete pod or PVC: {e}")


def check_pod_logs(
    api: client.CoreV1Api, pod_name: str, namespace: str, container_name: str = None, tail_lines: int = None
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
    try:
        return api.read_namespaced_pod_log(
            name=pod_name, namespace=namespace, container=container_name, tail_lines=tail_lines
        )
    except ApiException as e:
        raise RuntimeError(f"Failed to get pod logs: {e}")
