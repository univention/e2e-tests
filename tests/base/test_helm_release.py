# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2026 Univention GmbH

import pytest

from e2e.helm import supplied_values

pytestmark = [
    pytest.mark.password_generation_off,
]


def revision(release_secret) -> int:
    return int(release_secret.metadata.labels["version"])


def test_release_holds_no_seed(k8s, release_name):
    release_secrets = k8s.get_helm_release_secrets(release_name)
    assert release_secrets, f'No Helm release Secret found for the release "{release_name}".'

    values = supplied_values(max(release_secrets, key=revision))
    secrets = (values.get("global") or {}).get("secrets") or {}

    # The charts generate passwords when the value is unset or true.
    assert secrets.get("generatePasswords") not in (None, True)
    assert not secrets.get("masterPassword")
