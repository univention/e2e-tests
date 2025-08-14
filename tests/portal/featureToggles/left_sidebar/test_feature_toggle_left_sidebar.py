# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH


import pytest

from e2e.decorators import retrying_slow


@pytest.mark.feature_toggle
@pytest.mark.feature_toggle_left_sidebar
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
@retrying_slow
def test_something_with_a_feature_toggle(navigate_to_home_page_logged_in):
    pass
