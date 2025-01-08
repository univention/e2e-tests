# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH


def add_release_prefix(name: str, release_name: str | None):
    """
    Adds the `release_prefix` to `name` consistent with our Helm charts.
    """
    if not release_name or release_name == name:
        return name
    return f"{release_name}-{name}"
