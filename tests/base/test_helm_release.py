# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2026 Univention GmbH

import pytest

from e2e.helm import supplied_values

pytestmark = [
    pytest.mark.development_environment,
    pytest.mark.acceptance_environment,
]


def revision(release_secret) -> int:
    return int(release_secret.metadata.labels["version"])


def test_release_holds_no_seed_when_password_generation_is_off(k8s, release_name):
    release_secrets = k8s.get_helm_release_secrets(release_name)
    assert release_secrets, f'No Helm release Secret found for the release "{release_name}".'

    values = supplied_values(max(release_secrets, key=revision))
    secrets = (values.get("global") or {}).get("secrets") or {}

    # The charts generate passwords when the value is unset or true.
    if secrets.get("generatePasswords") in (None, True):
        pytest.skip("The deployment generates passwords, so it needs the seed.")

    assert not secrets.get("masterPassword")
