# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH
import pytest


@pytest.mark.upgrade
def test_noop():
    assert True
