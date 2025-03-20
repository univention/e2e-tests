# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

"""
Utility functions to help with Kubernetes objects.
"""

from collections.abc import Sequence
from typing import NamedTuple

from kubernetes.client import models


def get_by_name(items: Sequence, name: str):
    item = next(i for i in items if i.name == name)
    return item


class SecretDetails(NamedTuple):
    name: str
    key: str


class UrlParts(NamedTuple):
    host: str
    port: int
    scheme: str


def get_secret_by_volume(
    pod_spec: models.V1PodSpec,
    container_name: str,
    volume_name: str,
) -> SecretDetails:
    secret_volume = get_by_name(pod_spec.volumes, name=volume_name)
    secret_name = secret_volume.secret.secret_name

    main_container = get_by_name(pod_spec.containers, name=container_name)
    volume_mount = get_by_name(main_container.volume_mounts, name=volume_name)
    secret_key = volume_mount.sub_path

    return SecretDetails(name=secret_name, key=secret_key)
