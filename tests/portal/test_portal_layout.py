# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

from collections import defaultdict

import pytest
import requests

from umspages.portal.home_page.logged_in import HomePageLoggedIn
from umspages.portal.login_page import LoginPage


def get_portal_layout(page, user, user_password, navigation_api_url, admin=False):
    layout = defaultdict(list)

    login_page = LoginPage(page)
    login_page.login(user, user_password)

    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_in.assert_logged_in()

    layout["tiles"] = [tile.inner_text() for tile in home_page_logged_in.page.locator(".portal-tile__name").all()]

    # Fill sidebar entries
    home_page_logged_in.reveal_area(home_page_logged_in.right_side_menu, home_page_logged_in.header.hamburger_icon)
    layout["sidebar"] = home_page_logged_in.right_side_menu.get_all_sidebar_entries_text()
    home_page_logged_in.hide_area(home_page_logged_in.right_side_menu, home_page_logged_in.header.hamburger_icon)

    ## Fill central navigation entries
    response = requests.get(navigation_api_url)
    assert response.status_code == requests.codes.ok

    layout["central_navigation"] = {}
    for category in response.json()["categories"]:
        layout["central_navigation"][category["display_name"]] = []
        for entry in category["entries"]:
            layout["central_navigation"][category["display_name"]].append(entry["display_name"])

    return layout


@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_admin_portal_layout(navigate_to_login_page, admin_username, admin_password, subtests, navigation_api_url):
    page = navigate_to_login_page
    admin_layout = get_portal_layout(page, admin_username, admin_password, navigation_api_url, admin=True)

    expected_tiles = [
        "Keycloak",
        # "Welcome!",
        "Users",
        "Groups",
        "Computers",
        "Contacts",
        "Groups",
        "Users",
        "Computers",
        "Printers",
        "Blocklists",
        "DHCP",
        "DNS",
        "LDAP directory",
        "Mail",
        "Networks",
        "Policies",
        "Shares",
        "Portal",
        # "Welcome!",
    ]

    for tile in expected_tiles:
        with subtests.test(msg=f"tile {tile}"):
            assert tile in admin_layout["tiles"]

    # no extra tiles
    with subtests.test(msg="no extra tiles"):
        extra_tiles = set(admin_layout["tiles"]) - set(expected_tiles)
        assert extra_tiles == set()

    expected_sidebar = {
        "Certificates": ["Root certificate", "Certificate revocation list"],
        "Change Language": ["Deutsch", "English"],
        "Help": ["Univention Forum (Help)", "Feedback", "Univention Blog", "Univention Website"],
        "User settings": ["Change your password", "Protect your account", "My Profile"],
    }

    for section, items in expected_sidebar.items():
        with subtests.test(msg=f"sidebar section {section}"):
            assert section in admin_layout["sidebar"]
            for item in items:
                assert item in admin_layout["sidebar"][section]

    # no extra sidebar items
    with subtests.test(msg="no extra sidebar items"):
        extra_sidebar_items = set()
        for section, items in admin_layout["sidebar"].items():
            extra_items_from_section = set(items) - set(expected_sidebar[section])
            extra_sidebar_items.update(extra_items_from_section)
        assert extra_sidebar_items == set()

    # central navigation
    expected_central_navigation = {
        "Administration": ["System and domain settings"],
        "Applications": ["Login (Single sign-on)"],
    }

    with subtests.test(msg="central navigation"):
        assert "central_navigation" in admin_layout
        for section, items in expected_central_navigation.items():
            assert section in admin_layout["central_navigation"]
            for item in items:
                assert item in admin_layout["central_navigation"][section]

    # no extra central navigation items

    with subtests.test(msg="no extra central navigation items"):
        extra_central_navigation_items = set()
        for section, items in admin_layout["central_navigation"].items():
            extra_items_from_section = set(items) - set(expected_central_navigation[section])
            extra_central_navigation_items.update(extra_items_from_section)
        assert extra_central_navigation_items == set()


@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_regular_user_portal_layout(
    navigate_to_login_page,
    user,
    user_password,
    subtests,
    navigation_api_url,
):
    page = navigate_to_login_page
    user_layout = get_portal_layout(page, user.properties["username"], user_password, navigation_api_url)

    expected_tiles = []

    for tile in expected_tiles:
        with subtests.test(msg=f"tile {tile}"):
            assert tile in user_layout["tiles"]

    # no extra tiles
    with subtests.test(msg="no extra tiles"):
        extra_tiles = set(user_layout["tiles"]) - set(expected_tiles)
        assert extra_tiles == set()

    expected_sidebar = {
        "User settings": ["Change your password", "Protect your account", "My Profile"],
        "Certificates": ["Root certificate", "Certificate revocation list"],
        "Change Language": ["Deutsch", "English"],
        "Help": ["Univention Forum (Help)", "Feedback", "Univention Blog", "Univention Website"],
    }

    for item, expected in expected_sidebar.items():
        with subtests.test(msg=f"sidebar item {item}"):
            assert item in user_layout["sidebar"]
            assert user_layout["sidebar"][item] == expected

    # no extra sidebar items
    with subtests.test(msg="no extra sidebar items"):
        extra_sidebar_items = set()
        for section, items in user_layout["sidebar"].items():
            extra_items_from_section = set(items) - set(expected_sidebar[section])
            extra_sidebar_items.update(extra_items_from_section)
        assert extra_sidebar_items == set()

    # central navigation
    expected_central_navigation = {
        "Administration": ["System and domain settings"],
        "Applications": ["Login (Single sign-on)"],
    }

    with subtests.test(msg="central navigation"):
        assert "central_navigation" in user_layout
        for section, items in expected_central_navigation.items():
            assert section in user_layout["central_navigation"]
            for item in items:
                assert item in user_layout["central_navigation"][section]

    # no extra central navigation items

    with subtests.test(msg="no extra central navigation items"):
        extra_central_navigation_items = set()
        for section, items in user_layout["central_navigation"].items():
            extra_items_from_section = set(items) - set(expected_central_navigation[section])
            extra_central_navigation_items.update(extra_items_from_section)
        assert extra_central_navigation_items == set()
