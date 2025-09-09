# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import re

import pytest
from playwright.sync_api import expect

from e2e.decorators import retrying_slow
from umspages.portal.home_page.logged_in import HomePageLoggedIn


@pytest.mark.selfservice
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_user_can_access_2fa_selfservice(navigate_to_home_page_logged_in):
    assert_user_can_access_2fa_page(navigate_to_home_page_logged_in)


@pytest.mark.selfservice
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_admin_can_access_2fa_selfservice(navigate_to_home_page_logged_in_as_admin):
    assert_user_can_access_2fa_page(navigate_to_home_page_logged_in_as_admin)


@pytest.mark.selfservice
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_admin_can_access_2fa_admin_page(navigate_to_home_page_logged_in_as_admin):
    assert_user_can_access_2fa_page(
        navigate_to_home_page_logged_in_as_admin,
        tile_name_fragment="2FA Admin",
        title_name_fragment="Administrator: 2FA",
        heading_name_fragment="Admin",
        url_fragment="2fa/admin",
    )


@retrying_slow
def assert_user_can_access_2fa_page(
    page,
    tile_name_fragment="2FA Selfservice",
    title_name_fragment="Self-Service: 2FA",
    heading_name_fragment="Self",
    url_fragment="2fa/self-service",
):
    """
    Test that verifies a user can log in, click on the wanted 2FA icon,
    which opens a new tab with the 2FA UI.

    Args:
        page (Page): The Playwright page object representing the current browser page.
        tile_name_fragment (str): A fragment of the name of the wanted 2FA tile to locate it on the home page.
        title_name_fragment (str): A fragment of the title of the wanted 2FA page to verify it has loaded correctly.
        heading_name_fragment (str): A fragment of the heading of the wanted 2FA page to verify it is displayed correctly.
        url_fragment (str): A fragment of the URL of the wanted 2FA page to verify it has loaded correctly.
    """
    home_page_logged_in = HomePageLoggedIn(page)

    # Verify that we are on the home page and logged in
    home_page_logged_in.assert_logged_in()

    # Find the 2FA tile and click on it (which will open in a new tab)
    # Using get_new_tab to handle the new tab that opens
    # Support for both English and German interfaces
    try:
        twofa_tile = home_page_logged_in.page.get_by_role("link", name=re.compile(tile_name_fragment))
        expect(twofa_tile).to_be_visible()
    except AssertionError:
        page.reload()
        raise

    new_tab = home_page_logged_in.get_new_tab(twofa_tile)

    # Verify that the new tab has loaded with the correct URL
    expect(new_tab).to_have_url(re.compile(url_fragment))

    # Check that the page title starts with title_name_fragment
    expect(new_tab).to_have_title(re.compile(title_name_fragment))

    # Check for specific UI elements on the 2FA page
    # Looking for common elements that should be present on the 2FA page
    expect(new_tab.get_by_role("heading", name=re.compile(heading_name_fragment))).to_be_visible()

    # Check for common interactive elements on the page
    expect(new_tab.get_by_role("button", name=re.compile("Token")).first).to_be_visible()
