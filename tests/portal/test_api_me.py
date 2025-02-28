# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from e2e.api.portal_server import PortalServerApi
from umspages.portal.home_page.base import HomePage


def test_returns_empty_object_when_not_logged_in(page):
    home_page = HomePage(page)
    home_page.navigate()
    api = PortalServerApi(page.request)
    result = api.get("me").json()
    assert result == {}


def test_returns_user_details_for_a_regular_user(user, navigate_to_home_page_logged_in):
    page = navigate_to_home_page_logged_in
    api = PortalServerApi(page.request)
    result = api.get("me").json()
    assert result["user"]["username"] == user.properties["username"]
