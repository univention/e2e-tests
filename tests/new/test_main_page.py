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
from playwright.sync_api import expect

from pom.main_page import MainPage


@pytest.mark.gaia
@pytest.mark.devenv
class TestMainPage:
    def test_portal_main_page_design(
        self,
        main_page: MainPage,
        localization: dict,
    ):
        page = main_page

        assert page.title == "Sovereign Workplace"

        expect(page.category_1).to_be_visible()
        expect(page.login_widget).to_be_visible()
        expect(page.search).to_be_visible()
        expect(page.bell).to_be_visible()
        expect(page.menu_icon).to_be_visible()

        # Check Login menu
        expect(page.menu_login_button).not_to_be_visible()
        page.menu_icon.click()
        expect(page.menu_login_button).to_be_visible()

        # Check localization
        loc = localization
        assert page.lang == loc.lang

        loc = loc.main_page
        # Check the page title
        assert page.header == loc.PAGE_HEADER

        # Check widgets title. There are two categories.
        assert (
            page.category_1.locator(".portal-tile__name").inner_text()
            == loc.CATEGORY_1_LOGIN_WIDGET_TITLE
        )

        # Check right side menu text
        assert page.menu_login_button.inner_text() == loc.MENU_LOGIN_BUTTON_TEXT

    def test_portal_main_page_login_widget(self, main_page: MainPage):
        main_page.login_widget.click()
        expect(main_page._page).to_have_title("Sign in to souvap")

    def test_portal_main_page_side_menu_login(self, main_page: MainPage):
        main_page.menu_icon.click()
        main_page.menu_login_button.click()
        expect(main_page._page).to_have_title("Sign in to souvap")
