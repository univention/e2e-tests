# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH


from dataclasses import dataclass

import pytest
from playwright.sync_api import expect

from e2e.decorators import retrying_slow


@dataclass
class TileData:
    tile_name: str
    link: str


@pytest.mark.feature_toggle
@pytest.mark.feature_toggle_left_sidebar
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
@retrying_slow
def test_left_sidebar_contains_expected_links(navigate_to_home_page_logged_in_as_admin):
    page = navigate_to_home_page_logged_in_as_admin

    # Check if the waffle icon button is visible
    waffle_icon_button = page.get_by_role("button", name="Open sidebar navigation")
    expect(waffle_icon_button).to_be_visible()

    # Get all tiles in the Administration section
    admin_tiles = collect_portal_tiles(page, "Administration")
    admin_tiles.extend(collect_portal_tiles(page, "Applications"))

    # Click the waffle icon to open the sidebar and collect all links
    waffle_icon_button.click()
    sidebar_links = page.locator(".portal-left-sidenavigation__link")
    sidebar_links.first.wait_for(state="visible", timeout=5000)

    sidebar_entries = []
    for i in range(sidebar_links.count()):
        link = sidebar_links.nth(i)
        sidebar_entries.append(TileData(tile_name=link.text_content(), link=link.get_attribute("href")))

    # Compare link entries to admin tiles
    assert len(sidebar_entries) == len(admin_tiles), "Expected sidebar links count does match tiles count."
    for admin_tile in admin_tiles:
        assert admin_tile in sidebar_entries, f"Expected sidebar entry for '{admin_tile.tile_name}' not found."


def collect_portal_tiles(page, section):
    heading = page.get_by_role("heading", name=section)
    section = heading.locator("..")
    tiles = section.get_by_role("link")

    tile_entries = []
    for i in range(tiles.count()):
        tile = tiles.nth(i)
        tile_entries.append(
            TileData(tile_name=tile.locator(".portal-tile__name").text_content(), link=tile.get_attribute("href"))
        )

    return tile_entries


@pytest.mark.feature_toggle
@pytest.mark.feature_toggle_left_sidebar
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
# @retrying_slow
def test_left_sidebar_is_not_accessible_if_no_tiles_exist(navigate_to_home_page_logged_in_user_without_groups):
    page = navigate_to_home_page_logged_in_user_without_groups

    # Ensure waffle icon button is not visible
    waffle_icon_button = page.get_by_role("button", name="Open sidebar navigation")
    expect(waffle_icon_button).not_to_be_visible()
