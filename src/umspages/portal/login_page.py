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

from ..common.base import expect
from .common.portal_page import PortalPage
from .home_page.logged_out import HomePageLoggedOut


# TODO: Split into UCSLoginPage and KeycloakLoginPage
class LoginPage(PortalPage):
    def set_content(self, *args, **kwargs):
        super().set_content(*args, **kwargs)
        # TODO: Using regular expr to target different langs in SouvAP env. Needs better solution.
        # In headed mode, default language is English. In headless mode, it is Deutsch.
        self.username_input = self.page.get_by_label(re.compile("^(Username|Benutzername)"))
        self.password_input = self.page.get_by_label(re.compile("^Passwor(d|t)"))
        # TODO: Using regular expression to target both UCS and SouvAP envs. Needs a better solution.
        self.login_button = self.page.get_by_role("button", name=re.compile("^(Login|Sign In|Anmelden)"))
        # Keycloak login specific

        # TODO: Missing role in the sources
        # Should use "page.get_by_role("dialog", ...)" instead
        self.cookie_dialog = self.page.locator(".cookie-banner .dialog")

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
        self.click_login_button()
