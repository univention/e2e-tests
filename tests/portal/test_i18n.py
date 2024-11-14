# Like what you see? Join us!
# https://www.univention.com/about-us/careers/vacancies/
#
# Copyright 2001-2023 Univention GmbH
#
# https://www.univention.de/
#
# All rights reserved.
#
# The source code of this program is made available
# under the terms of the GNU Affero General Public License version 3
# (GNU AGPL V3) as published by the Free Software Foundation.
#
# Binary versions of this program provided by Univention to you as
# well as other copyrighted, protected or trademarked materials like
# Logos, graphics, fonts, specific documentations and configurations,
# cryptographic keys etc. are subject to a license agreement between
# you and Univention and not subject to the GNU AGPL V3.
#
# In the case you use this program under the terms of the GNU AGPL V3,
# the program is provided in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License with the Debian GNU/Linux or Univention distribution in file
# /usr/share/common-licenses/AGPL-3; if not, see
# <https://www.gnu.org/licenses/>.

import re

import pytest

from umspages.common.base import expect
from umspages.portal.home_page.logged_in import HomePageLoggedIn
from umspages.portal.home_page.logged_out import HomePageLoggedOut
from umspages.portal.users.users_page import UCSUsersPage


@pytest.mark.i18n
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_anonymous_user_can_switch_language_to_german(navigate_to_home_page_logged_out):
    page = navigate_to_home_page_logged_out
    home_page = HomePageLoggedOut(page)
    home_page.switch_language("Deutsch")

    assert home_page.get_language() == "de"

    home_page.reveal_area(home_page.right_side_menu, home_page.header.hamburger_icon)
    expect(home_page.right_side_menu.menu_entry("Sprache ändern")).to_be_visible()
    expect(home_page.header.page_part_locator.get_by_role("button", name="Suche")).to_be_visible()


@pytest.mark.i18n
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_anonymous_user_can_switch_language_to_english(navigate_to_home_page_logged_out):
    page = navigate_to_home_page_logged_out
    home_page = HomePageLoggedOut(page)
    home_page.switch_language("Deutsch")
    home_page.switch_language("English")

    assert home_page.get_language() == "en"

    home_page.reveal_area(home_page.right_side_menu, home_page.header.hamburger_icon)
    expect(home_page.right_side_menu.menu_entry("Change Language")).to_be_visible()
    expect(home_page.header.page_part_locator.get_by_role("button", name="Search")).to_be_visible()


@pytest.mark.i18n
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_logged_in_user_can_switch_language_to_german(navigate_to_home_page_logged_in):
    """
    This test checks if a logged in user can switch the language to German.

    1. Logs in with a user.
    2. Switches the language to German.
    3. Checks if the language is set to German.
    4. Checks if the language switch is now in German.
    5. Reloads the page.
    6. Checks if the Users tile is now in German.
    7. Clicks the Users tile.
    8. Check the UMC Add button is now in German.
    """
    page = navigate_to_home_page_logged_in
    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_in.switch_language("Deutsch")

    assert home_page_logged_in.get_language() == "de"

    home_page_logged_in.reveal_area(home_page_logged_in.right_side_menu, home_page_logged_in.header.hamburger_icon)
    expect(home_page_logged_in.right_side_menu.menu_entry("Sprache ändern")).to_be_visible()
    # FIXME: Right now, Favourites is not translated until reload.
    # Same goes for UMC tiles.
    home_page_logged_in.page.reload()
    german_users_tile = home_page_logged_in.page.get_by_role(
        "link", name=re.compile("Benutzer New Tab|Benutzer iFrame")
    ).first
    expect(german_users_tile).to_be_visible()
    german_users_tile.click()
    users_iframe = home_page_logged_in.page.frame_locator('iframe[title="Benutzer"]')
    expect(users_iframe.get_by_role("button", name="Hinzufügen")).to_be_visible(timeout=10000)


@pytest.mark.i18n
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_logged_in_user_can_switch_language_to_english(navigate_to_home_page_logged_in):
    """
    This test checks if a logged in user can switch the language to English.

    1. Logs in with a user.
    2. Switches the language to English.
    3. Checks if the language is set to English.
    4. Checks if the language switch is now in English.
    5. Reloads the page.
    6. Checks if the Users tile is now in English.
    7. Clicks the Users tile.
    8. Check the UMC Add button is now in English.
    """
    page = navigate_to_home_page_logged_in
    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_in.switch_language("Deutsch")
    assert home_page_logged_in.get_language() == "de"
    home_page_logged_in.switch_language("English")
    assert home_page_logged_in.get_language() == "en"

    home_page_logged_in.reveal_area(home_page_logged_in.right_side_menu, home_page_logged_in.header.hamburger_icon)
    expect(home_page_logged_in.right_side_menu.menu_entry("Change Language")).to_be_visible()
    home_page_logged_in.page.reload()
    expect(home_page_logged_in.users_tile).to_be_visible()

    home_page_logged_in.users_tile.click()
    users_page = UCSUsersPage(home_page_logged_in.page)
    expect(users_page.add_user_button).to_be_visible(timeout=10000)
