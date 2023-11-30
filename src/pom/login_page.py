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

from playwright.sync_api import Locator, Page

from pom.base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self._lang = page.locator("html").get_attribute("lang")
        self._title = page.locator("head").locator("title").inner_text()

        self._username_input: Locator = None
        self._password_input: Locator = None
        self._login_btn: Locator = None

    @property
    def lang(self) -> str:
        return self._lang

    @lang.setter
    def lang(self, value: str):
        self._lang = value

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        self._title = value

    @property
    def header(self) -> str:
        return self._header

    @header.setter
    def header(self, value: str):
        self._header = value

    @property
    def username_input(self) -> Locator:
        return self._username_input

    @username_input.setter
    def username_input(self, value: Locator):
        self._username_input = value

    @property
    def password_input(self) -> Locator:
        return self._password_input

    @password_input.setter
    def password_input(self, value: Locator):
        self._password_input = value

    @property
    def login_button(self) -> Locator:
        return self._login_btn

    @login_button.setter
    def login_button(self, value: Locator):
        self._login_btn = value

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        self._page.wait_for_selector('#app')


class GaiaLoginPage(LoginPage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.header = page.locator('#kc-page-title').inner_text()
        self.username_input_label = page.locator('label[for="username"]').inner_text()
        self.password_input_label = page.locator('label[for="password"]').inner_text()
        self.username_input = page.locator('#kc-form-login').locator('#username')
        self.password_input = page.locator('#kc-form-login').locator('#password')
        self.login_button = page.locator('#kc-form-login').locator('#kc-login')


class DevenvLoginPage(LoginPage):
    def __init__(self, page: Page):
        super().__init__(page)

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
