# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import secrets
from typing import Optional

from kubernetes.dynamic import DynamicClient
from kubernetes.dynamic.resource import ResourceInstance


class ChaosMeshFixture:
    """
    This fixture helps to deploy Chaos Mesh related resouces.

    The implementation does not aim to be feature complete. Only the user
    features are supported. This also means that it is only generic enough for
    the current usage.

    Method names for experiments are based on the field `spec.action` and the
    type of the chaos experiment. Duplication of prefixes is avoided, e.g.
    using `pod_kill` instead of `pod_pod_kill`.

    The chaos experiment target based on various supported selectors. The used
    ones are provided as keyword parameters for the method with case handling
    adjusted to Python's conventions, e.g. `label_selector` for the field
    `spec.selector.labelSelectors`.

    See: https://chaos-mesh.org/docs.
    """

    def __init__(self, client: DynamicClient, namespace: str):
        self.client = client
        self.namespace = namespace
        self._to_cleanup = []

    def pod_kill(self, label_selectors: Optional[dict]):
        pod_chaos = {
            "apiVersion": "chaos-mesh.org/v1alpha1",
            "kind": "PodChaos",
            "metadata": {
                "name": secrets.token_hex(16),
            },
            "spec": {
                "action": "pod-kill",
                "gracePeriod": 1,
                "mode": "one",
                "selector": {},
            },
        }

        if label_selectors:
            pod_chaos["spec"]["selector"]["labelSelectors"] = label_selectors

        pod_chaos_resource = self._get_resource_from_instance(pod_chaos)
        result = pod_chaos_resource.create(body=pod_chaos, namespace=self.namespace)
        self._add_to_cleanup(result)
        return Experiment(result)

    def cleanup(self):
        for item in self._to_cleanup:
            self._delete_resource_instance(item)

    def _add_to_cleanup(self, item):
        self._to_cleanup.append(item)

    def _delete_resource_instance(self, instance):
        resource = self._get_resource_from_instance(instance)
        resource.delete(
            name=instance["metadata"]["name"],
            namespace=instance["metadata"]["namespace"],
        )

    def _get_resource_from_instance(self, instance: dict | ResourceInstance):
        # Using only dict based access to ensure that this works both for a
        # ResourceInstance and a dict.
        resource = self.client.resources.get(
            api_version=instance["apiVersion"],
            kind=instance["kind"],
        )
        return resource


class Experiment:
    """
    Represents one running experiment.

    This abstracts over the result of the Kubernetes API client.
    """

    def __init__(self, instance: ResourceInstance):
        self.instance = instance