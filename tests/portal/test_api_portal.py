# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import pytest

from e2e.api.portal_server import PortalServerApi
from umspages.portal.home_page.base import HomePage


@pytest.mark.parametrize(
    "portal_link_list",
    [
        "corner_links",
        "menu_links",
        "quick_links",
        "user_links",
    ],
)
def test_result_contains_quick_links(page, portal_link_list):
    home_page = HomePage(page)
    home_page.navigate()
    api = PortalServerApi(page.request)
    result = api.get_portal().json()
    assert portal_link_list in result
