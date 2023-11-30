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

from pom.home_user_page import AdminHomePage, UserHomePage
from pom.main_page import MainPage
from pom.page_menu import AdminToolbarMenu, MainToolbarMenu, UserToolbarMenu


@pytest.mark.devenv
@pytest.mark.gaia
class TestGaiaPageMenu:
    def test_portal_main_page_menu(
            self,
            main_page: MainPage,
            localization: dict,
    ):
        main_page.menu_icon.click()
        side_menu = MainToolbarMenu(main_page)

        expect(side_menu.language_button).to_be_visible()
        expect(side_menu.privacy_button).to_be_visible()
        expect(side_menu.legalnotice_button).to_be_visible()

        loc = localization.side_menu

        assert loc.MENU_CHANGE_LENGUAGE_TEXT in side_menu.language_button.inner_text()
        assert loc.MENU_PRIVACY_BUTTON_TEXT in side_menu.privacy_button.inner_text()
        assert loc.MENU_LEGAL_BUTTON_TEXT in side_menu.legalnotice_button.inner_text()

    def test_portal_admin_home_page_menu(
            self,
            admin_home_page: AdminHomePage,
            localization: dict,
    ):
        admin_home_page.menu_icon.click()
        side_menu = AdminToolbarMenu(admin_home_page)

        expect(side_menu.settings_button).to_be_visible()
        expect(side_menu.language_button).to_be_visible()
        expect(side_menu.privacy_button).to_be_visible()
        expect(side_menu.legalnotice_button).to_be_visible()

        loc = localization.side_menu

        assert loc.MENU_USER_SETTINGS_TEXT in side_menu.settings_button.inner_text()
        assert loc.MENU_CHANGE_LENGUAGE_TEXT in side_menu.language_button.inner_text()
        assert loc.MENU_PRIVACY_BUTTON_TEXT in side_menu.privacy_button.inner_text()
        assert loc.MENU_LEGAL_BUTTON_TEXT in side_menu.legalnotice_button.inner_text()

        # TODO: submenu checks
        '''
        side_menu.settings_button.click()
        update_password_button = admin_home_page._page.locator('.portal-sidenavigation__menu-subItem').locator(
            '[href*="selfservice/passwordchange"]')

        expect(update_password_button).to_be_visible()
        assert loc.SUBMENU_UPDATE_PASSWORD_TEXT in update_password_button.inner_text()
        '''

    def test_portal_user_home_page_menu(
            self,
            user_home_page: UserHomePage,
            localization: dict,
    ):
        user_home_page.menu_icon.click()
        side_menu = UserToolbarMenu(user_home_page)

        expect(side_menu.settings_button).to_be_visible()
        expect(side_menu.language_button).to_be_visible()
        expect(side_menu.privacy_button).to_be_visible()
        expect(side_menu.legalnotice_button).to_be_visible()

        loc = localization.side_menu

        assert loc.MENU_USER_SETTINGS_TEXT in side_menu.settings_button.inner_text()
        assert loc.MENU_CHANGE_LENGUAGE_TEXT in side_menu.language_button.inner_text()
        assert loc.MENU_PRIVACY_BUTTON_TEXT in side_menu.privacy_button.inner_text()
        assert loc.MENU_LEGAL_BUTTON_TEXT in side_menu.legalnotice_button.inner_text()
