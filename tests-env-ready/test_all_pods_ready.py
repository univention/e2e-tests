# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import os
import time
from dataclasses import dataclass
from datetime import timedelta

import kubernetes
import pytest


@dataclass
class Config:
    namespace: str
    min_ready: int
    stable_seconds: timedelta
    timeout: timedelta
    watch_slice: timedelta


@pytest.fixture(scope="session")
def config() -> Config:
    return Config(
        namespace=os.environ["DEPLOY_NAMESPACE"],
        min_ready=20,
        stable_seconds=timedelta(seconds=15),
        timeout=timedelta(seconds=60),
        watch_slice=timedelta(seconds=30),
    )


@pytest.fixture
def k8s() -> kubernetes.client.CoreV1Api:
    try:
        kubernetes.config.load_kube_config()
    except Exception:
        kubernetes.config.load_incluster_config()
    return kubernetes.client.CoreV1Api()


def test_pods_ready_with_watch(corev1, namespace):
    wait_with_watch(corev1, namespace)


def pod_healthy(pod) -> bool:
    """
    A Pod counts as 'healthy' if:
      - phase == Running AND Ready condition True, OR
      - phase == Succeeded (Completed job).
    """
    phase = (pod.status.phase or "").lower()
    if phase == "running":
        conditions = pod.status.conditions or []
        return any(c.type == "Ready" and c.status == "True" for c in conditions)
    if phase == "succeeded":
        return True
    return False


def snapshot_pods(corev1, namespace):
    lst = corev1.list_namespaced_pod(namespace=namespace)
    state = {}
    for p in lst.items:
        # track only non-terminal pods
        if not is_terminal(p):
            state[p.metadata.name] = dict(
                ready=ready_flag(p),
                rv=p.metadata.resource_version,
            )
    # list.metadata.resource_version is the correct RV to resume the watch
    rv = lst.metadata.resource_version
    return state, rv


def readiness_ok(state: dict) -> tuple[bool, int, list[str]]:
    ready_count = sum(1 for v in state.values() if v["ready"])
    non_term = len(state)
    ok = (non_term > 0) and (ready_count == non_term) and (ready_count >= MIN_READY)
    not_ready = sorted([name for name, v in state.items() if not v["ready"]])
    return ok, ready_count, not_ready


def wait_with_watch(corev1, namespace: str):
    # initialize state and resourceVersion
    state, rv = snapshot_pods(corev1, namespace)
    start = time.monotonic()
    stable_start = None
    watch = kubernetes.watch.Watch()

    while True:
        # evaluate current condition before (re)starting the watch slice
        ok, ready_count, not_ready = readiness_ok(state)
        if ok:
            if stable_start is None:
                stable_start = time.monotonic()
            elif time.monotonic() - stable_start >= STABLE_SECONDS:
                return  # success
        else:
            stable_start = None

        if time.monotonic() - start > OVERALL_TIMEOUT:
            raise AssertionError(
                f"Timed out after {OVERALL_TIMEOUT}s. "
                f"non_terminal={len(state)} ready={ready_count} not_ready={not_ready}"
            )

        # consume one server-side watch "slice" so we never block forever
        try:
            for evt in watch.stream(
                corev1.list_namespaced_pod,
                namespace=namespace,
                resource_version=rv,
                timeout_seconds=WATCH_SLICE_SECONDS,
            ):
                typ = evt["type"]  # "ADDED" | "MODIFIED" | "DELETED" | "BOOKMARK"
                obj = evt["object"]

                # Keep rv advancing
                if obj.metadata and obj.metadata.resource_version:
                    rv = obj.metadata.resource_version

                if typ == "BOOKMARK":
                    # no object status changes; continue
                    continue

                name = obj.metadata.name

                if typ == "DELETED" or is_terminal(obj):
                    # stop tracking if pod deleted or became terminal
                    state.pop(name, None)
                else:
                    # track/update non-terminal pod
                    state[name] = dict(
                        ready=ready_flag(obj),
                        rv=obj.metadata.resource_version,
                    )

                # quick, cheap check after each event
                ok, ready_count, _ = readiness_ok(state)
                if ok:
                    if stable_start is None:
                        stable_start = time.monotonic()
                    elif time.monotonic() - stable_start >= STABLE_SECONDS:
                        return
                else:
                    stable_start = None

                if time.monotonic() - start > OVERALL_TIMEOUT:
                    raise AssertionError(
                        f"Timed out after {OVERALL_TIMEOUT}s. " f"non_terminal={len(state)} ready={ready_count}"
                    )

        except Exception:
            # On RV compaction or transient errors, take a fresh snapshot and continue
            state, rv = snapshot_pods(corev1, namespace)
