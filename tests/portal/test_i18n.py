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

import pytest

from umspages.common.base import expect
from umspages.portal.home_page.logged_out import HomePageLoggedOut


@pytest.mark.i18n
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_user_can_switch_language_to_german(navigate_to_home_page_logged_out):
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
def test_user_can_switch_language_to_english(navigate_to_home_page_logged_out):
    page = navigate_to_home_page_logged_out
    home_page = HomePageLoggedOut(page)
    home_page.switch_language("Deutsch")
    home_page.switch_language("English")

    assert home_page.get_language() == "en"

    home_page.reveal_area(home_page.right_side_menu, home_page.header.hamburger_icon)
    expect(home_page.right_side_menu.menu_entry("Change Language")).to_be_visible()
    expect(home_page.header.page_part_locator.get_by_role("button", name="Search")).to_be_visible()
