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

from ..common.base import BasePage, expect
from .welcome_page import WelcomePage


class AdminLoginPage(BasePage):
    def set_content(self, *args, **kwargs):
        super().set_content(*args, **kwargs)
        self.username_input = self.page.get_by_label("Username or email")
        self.password_input = self.page.get_by_label("Password")
        self.submit_button = self.page.get_by_role("button", name="Sign In")
        self.invalid_login_message = self.page.get_by_text(
            "Invalid username or password.")

    def is_displayed(self):
        expect(self.username_input).to_be_visible()

    def navigate(self):
        welcome_page = WelcomePage(self.page)
        welcome_page.navigate()
        welcome_page.click_administrator_console_link()

    def fill_username(self, username):
        self.username_input.fill(username)

    def fill_password(self, password):
        self.password_input.fill(password)

    def click_submit_button(self):
        self.submit_button.click()

    def login(self, username, password):
        self.fill_username(username)
        self.fill_password(password)
        self.click_submit_button()
