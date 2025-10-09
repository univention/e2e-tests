# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

"""
Debug tests for testing pytest_retry script behavior.

These tests are marked with 'debug_test' and 'acceptance_environment'
to ensure they can be run with the standard CI test selection.
"""

import pytest


@pytest.mark.debug_test
@pytest.mark.acceptance_environment
def test_debug_always_passes():
    """Debug test that always passes."""
    assert True, "This test should always pass"


@pytest.mark.debug_test
@pytest.mark.acceptance_environment
def test_debug_always_fails():
    """Debug test that always fails."""
    assert False, "This test is designed to always fail for debugging pytest_retry"
