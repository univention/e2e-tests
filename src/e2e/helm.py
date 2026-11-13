# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import base64
import gzip
import json


def add_release_prefix(name: str, release_name: str | None):
    """
    Adds the `release_prefix` to `name` consistent with our Helm charts.
    """
    if not release_name or release_name == name:
        return name
    return f"{release_name}-{name}"


def supplied_values(release_secret) -> dict:
    """
    Returns the values that were passed to Helm for one revision of a release.

    Helm base64-encodes the gzipped release, and Kubernetes base64-encodes it again.
    """
    payload = base64.b64decode(base64.b64decode(release_secret.data["release"]))
    release = json.loads(gzip.decompress(payload))
    return release.get("config") or {}
