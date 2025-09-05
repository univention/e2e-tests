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
import pytest

logger = logging.getLogger()


@dataclass
class Config:
    namespace: str
    min_ready: int
    stable_seconds: int
    timeout: int


def _config() -> Config:
    return Config(
        namespace=os.environ["DEPLOY_NAMESPACE"],
        min_ready=20,
        stable_seconds=15,
        timeout=60,
    )


def _k8s_corev1() -> kubernetes.client.CoreV1Api:
    try:
        kubernetes.config.load_kube_config()
    except Exception:
        kubernetes.config.load_incluster_config()
    return kubernetes.client.CoreV1Api()


@pytest.fixture(scope="session")
def config() -> Config:
    return _config()


@pytest.fixture
def k8s_corev1() -> kubernetes.client.CoreV1Api:
    return _k8s_corev1()


def main():
    logging.basicConfig(level="DEBUG", format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    wait_with_watch(_k8s_corev1(), _config())


def test_pods_ready_with_watch(k8s_corev1: kubernetes.client.CoreV1Api, config: Config) -> None:
    wait_with_watch(k8s_corev1, config)


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


def parse_pod_manifest(manifest: kubernetes.client.V1Pod) -> PodStatus:
    try:
        meta = manifest.metadata
        status_conditions = manifest.status.conditions

        name = meta.name

        owner_ref = meta.owner_references[0]
        controller_type = ControllerType(owner_ref.kind)
        controller_name = owner_ref.name

        if controller_type == ControllerType.Job:
            ready = any(cond.reason == "PodCompleted" and cond.status == "True" for cond in status_conditions)
        else:
            pod_ready = any(cond.type == "Ready" and cond.status == "True" for cond in status_conditions)

            containers_ready = True
            if manifest.status.container_statuses:
                containers_ready = all(container.ready for container in manifest.status.container_statuses)

            ready = pod_ready and containers_ready
        result = PodStatus(
            ready=ready,
            name=name,
            controller_name=controller_name,
            controller_type=controller_type,
        )
    except (KeyError, TypeError, ValueError) as e:
        logger.error("Could not parse Pod manifest into PodStatus: %s", e)
        raise ParsePodError(f"Invalid pod manifest for PodStatus: {e}") from e
    logger.debug("Parsed new Pod: %r", result)
    return result


class NamespaceStatus:
    status: dict[str, PodStatus]
    stable_since: float | None = None

    def __init__(self, config: Config) -> None:
        self.status = {}
        self.config = config

    def update(self, pod: PodStatus):
        if pod.controller_type == ControllerType.Job:
            self.status[pod.controller_name] = pod
            return
        self.status[pod.name] = pod

    def pods_ready(self) -> bool:
        if (pod_number := len(self.status)) < 20:
            logger.warning("Not enough pods deployed. number: %d", pod_number)
            return False

        ready = True
        for pod in self.status.values():
            if pod.ready is False:
                logger.warning("Pod not ready. name: %s, ready: %s", pod.name, pod.ready)
                ready = False
        return ready


class Timeout:
    """Linux-only timeout using signal.setitimer()."""

    def __init__(self, seconds: int, on_timeout: Callable[[], None]) -> None:
        self.seconds = seconds
        self.on_timeout = on_timeout
        self._armed = False

    def _handler(self, signum, frame):
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


def wait_with_watch(k8s_corev1: kubernetes.client.CoreV1Api, config: Config) -> None:
    watch: kubernetes.watch.Watch = kubernetes.watch.Watch()
    timeout = Timeout(config.timeout, (lambda: sys.exit(1)))
    timeout.set()

    def finished() -> None:
        print(f"Namespace: {config.namespace} is healthy")
        sys.exit(0)

    stable_timeout = Timeout(config.stable_seconds, finished)

    while True:
        status = NamespaceStatus(config)
        logger.info("watching for events")
        for event in watch.stream(
            k8s_corev1.list_namespaced_pod,
            namespace=config.namespace,
            timeout_seconds=120,
            allow_watch_bookmarks=True,
        ):
            type: str = event["type"]  # ADDED | MODIFIED | DELETED | BOOKMARK
            logger.debug("Event type: %s", type)
            if type == "BOOKMARK":
                continue

            pod_manifest: kubernetes.client.V1Pod = event["object"]
            try:
                pod = parse_pod_manifest(pod_manifest)
            except ParsePodError:
                stable_timeout.cancel()
                continue

            status.update(pod)
            if status.pods_ready() is False:
                stable_timeout.cancel()

            stable_timeout.set()


if __name__ == "__main__":
    main()
