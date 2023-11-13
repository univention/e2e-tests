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

from playwright.sync_api import Page

from ..common.base import BasePage


# from ..common.base import expect
# from .common.portal_page import PortalPage
from .home_page.logged_out import HomePageLoggedOut


class LoginPage(BasePage):
    def __init__(self, page: Page):
        BasePage.__init__(self, page)

        self.lang = page.locator("html").get_attribute("lang")
        self.title = page.locator("head").locator("title").inner_text()
        self.header = page.locator('.umcHeaderLeft').locator('h2').inner_text()
        self.login_title = page.locator('#umcLoginContent').locator('h2').inner_text()
        self.username_input = page.locator('#umcLoginUsername')
        self.username_input_label = page.locator('#umcLoginForm').locator('#umcLoginUsernameLabel').inner_text()
        self.password_input = page.locator('#umcLoginPassword')
        self.password_input_label = page.locator('#umcLoginForm').locator('#umcLoginPasswordLabel').inner_text()
        self.login_button = page.locator('#umcLoginForm').locator('.umcLoginFormButton')
        self.login_button_label = page.locator('#umcLoginForm').locator('.umcLoginFormButton').inner_text()
        self.menu = page.locator('span[widgetid="umc_menu_Button_0"]')
        self.help_button = page.locator('#umcMenuHelp')
        self.back_button = page.locator('#umc_menu_MenuItem_4')


    def navigate(self, cookies_accepted=False):
        home_page = HomePageLoggedOut(self.page)
        home_page.navigate(cookies_accepted=cookies_accepted)
        home_page.is_displayed()
        self.reveal_area(self.right_side_menu, self.header.hamburger_icon)
        expect(self.right_side_menu.login_button).to_be_visible()
        expect(self.right_side_menu.logout_button).to_be_hidden()
        self.right_side_menu.click_login_button()

    def navigate_saml(self):
        """Login via saml specifically"""
        home_page = HomePageLoggedOut(self.page)
        home_page.navigate()
        home_page.is_displayed()
        home_page.saml_login_tile.click()

    def is_displayed(self):
        expect(self.username_input).to_be_visible()

    def fill_username(self, username):
        self.username_input.fill(username)

    def fill_password(self, password):
        self.password_input.fill(password)

    def click_login_button(self):
        self.login_button.click()

    def login(self, username, password):
        self.fill_username(username)
        self.fill_password(password)
