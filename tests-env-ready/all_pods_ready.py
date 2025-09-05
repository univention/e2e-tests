#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import logging
import os
import signal
import sys
from dataclasses import dataclass
from enum import Enum
from typing import Callable

import kubernetes

logger = logging.getLogger()


@dataclass
class Config:
    namespace: str
    min_ready: int
    stable_seconds: int
    timeout: int


class Timeout:
    """Linux-only timeout using signal.setitimer()."""

    def __init__(self, seconds: int, on_timeout: Callable[[], None]) -> None:
        self.seconds = seconds
        self.on_timeout = on_timeout
        self._armed = False

    def _handler(self, signum: int, frame) -> None:
        self._armed = False
        self.on_timeout()

    def set(self) -> None:
        if self._armed:
            return
        signal.signal(signal.SIGALRM, self._handler)
        signal.setitimer(signal.ITIMER_REAL, self.seconds)
        self._armed = True

    def cancel(self) -> None:
        if self._armed:
            signal.setitimer(signal.ITIMER_REAL, 0)
            self._armed = False


class ControllerType(Enum):
    ReplicaSet = "ReplicaSet"
    StatefulSet = "StatefulSet"
    Job = "Job"


class ParsePodError(Exception): ...


@dataclass
class PodStatus:
    name: str
    ready: bool
    controller_name: str
    controller_type: ControllerType
    ready_containers: int
    total_containers: int
    status: str

    def format_status(self) -> str:
        return f"{self.name:<64} {self.ready_containers}/{self.total_containers}     {self.status:<17}"


def _get_container_counts(manifest: kubernetes.client.V1Pod) -> tuple[int, int]:
    """Returns (ready_containers, total_containers)"""
    total_containers = len(manifest.spec.containers) if manifest.spec.containers else 0
    ready_containers = 0
    if manifest.status.container_statuses:
        ready_containers = sum(1 for container in manifest.status.container_statuses if container.ready)
    return ready_containers, total_containers


def _is_pod_ready(manifest: kubernetes.client.V1Pod, controller_type: ControllerType, event_type: str) -> bool:
    """Determine if a pod is ready based on its type and status"""
    if event_type == "DELETED" or manifest.metadata.deletion_timestamp is not None:
        return False

    conditions = manifest.status.conditions or []
    if controller_type == ControllerType.Job:
        return any(cond.reason == "PodCompleted" and cond.status == "True" for cond in conditions)

    pod_ready = any(cond.type == "Ready" and cond.status == "True" for cond in conditions)
    containers_ready = True
    if manifest.status.container_statuses:
        containers_ready = all(container.ready for container in manifest.status.container_statuses)
    return pod_ready and containers_ready


def _get_pod_status_string(manifest: kubernetes.client.V1Pod, event_type: str) -> str:
    """Get kubectl-like status string for the pod"""
    if event_type == "DELETED":
        return "Deleted"

    if manifest.metadata.deletion_timestamp is not None:
        return "Terminating"

    pod_phase = manifest.status.phase if manifest.status.phase else "Unknown"

    if pod_phase == "Pending":
        # Check for init containers
        if manifest.status.init_container_statuses:
            total_init = len(manifest.spec.init_containers) if manifest.spec.init_containers else 0
            ready_init = sum(1 for container in manifest.status.init_container_statuses if container.ready)
            return f"Init:{ready_init}/{total_init}"
        # Check if PodInitializing
        elif manifest.status.container_statuses and any(not c.ready for c in manifest.status.container_statuses):
            return "PodInitializing"

    return pod_phase


def parse_pod_manifest(manifest: kubernetes.client.V1Pod, event_type: str) -> PodStatus:
    try:
        meta = manifest.metadata

        owner_ref = meta.owner_references[0]
        controller_type = ControllerType(owner_ref.kind)
        controller_name = owner_ref.name

        ready = _is_pod_ready(manifest, controller_type, event_type)
        ready_containers, total_containers = _get_container_counts(manifest)
        status_str = _get_pod_status_string(manifest, event_type)

        result = PodStatus(
            ready=ready,
            name=meta.name,
            controller_name=controller_name,
            controller_type=controller_type,
            ready_containers=ready_containers,
            total_containers=total_containers,
            status=status_str,
        )
    except (KeyError, TypeError, ValueError) as e:
        logger.error("Could not parse Pod manifest into PodStatus: %s", e)
        raise ParsePodError(f"Invalid pod manifest for PodStatus: {e}") from e
    return result


class NamespaceStatus:
    status: dict[str, PodStatus]

    def __init__(self) -> None:
        self.status = {}

    def update(self, pod: PodStatus) -> None:
        if pod.controller_type == ControllerType.Job:
            self.status[pod.controller_name] = pod
            return
        self.status[pod.name] = pod

    def delete(self, pod: PodStatus) -> None:
        if pod.controller_type == ControllerType.Job:
            self.status.pop(pod.controller_name, None)
            return
        self.status.pop(pod.name, None)

    def pods_ready(self, min_ready: int) -> bool:
        if len(self.status) < min_ready:
            return False

        return all(pod.ready for pod in self.status.values())


def wait_with_watch(k8s_corev1: kubernetes.client.CoreV1Api, config: Config) -> None:
    watch: kubernetes.watch.Watch = kubernetes.watch.Watch()

    def failed() -> None:
        logger.error("Timeout after %ds waiting for namespace %s to be ready", config.timeout, config.namespace)
        sys.exit(1)

    timeout = Timeout(config.timeout, failed)
    timeout.set()

    def finished() -> None:
        logger.info(f"Namespace: {config.namespace} is healthy")
        sys.exit(0)

    stable_timeout = Timeout(config.stable_seconds, finished)

    while True:
        # Recreate status on each watch loop to avoid stale state from missed/failed events.
        # Kubernetes streams all existing pods as ADDED events on watch restart, ensuring accuracy.
        status = NamespaceStatus()
        logger.info("watching for events")
        try:
            for event in watch.stream(
                k8s_corev1.list_namespaced_pod,
                namespace=config.namespace,
                timeout_seconds=120,
                allow_watch_bookmarks=True,
            ):
                event_type: str = event["type"]  # ADDED | MODIFIED | DELETED | BOOKMARK
                logger.debug("Event type: %s", event_type)
                if event_type == "BOOKMARK":
                    continue

                pod_manifest: kubernetes.client.V1Pod = event["object"]

                try:
                    pod = parse_pod_manifest(pod_manifest, event_type)
                except ParsePodError:
                    stable_timeout.cancel()
                    continue

                if event_type == "DELETED":
                    status.delete(pod)
                    stable_timeout.cancel()
                    continue

                status.update(pod)
                if status.pods_ready(config.min_ready) is False:
                    logger.warning("%-9s %s", event_type, pod.format_status())
                    stable_timeout.cancel()
                    continue

                logger.info("%-9s %s", event_type, pod.format_status())
                stable_timeout.set()
        except Exception as e:
            logger.warning("Watch stream failed, retrying: %s", e)
            stable_timeout.cancel()
            # Continue to next iteration of while loop to restart watch


def _k8s_corev1() -> kubernetes.client.CoreV1Api:
    try:
        kubernetes.config.load_kube_config()
    except Exception:
        kubernetes.config.load_incluster_config()
    return kubernetes.client.CoreV1Api()


def main():
    logging.basicConfig(level=os.environ["LOG_LEVEL"], format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s")

    _config = Config(
        namespace=os.environ["DEPLOY_NAMESPACE"],
        min_ready=20,
        stable_seconds=30,
        timeout=int(os.environ["TIMEOUT"]),
    )

    if _config.min_ready < 0:
        raise ValueError(f"min_ready must be >= 0, got {_config.min_ready}")
    if _config.timeout <= 0:
        raise ValueError(f"timeout must be > 0, got {_config.timeout}")

    wait_with_watch(_k8s_corev1(), _config)


if __name__ == "__main__":
    main()
