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

from ..common.base import BasePage


class LoginPage(BasePage):
    """
    Playwright page for Keycloak login page.
    """

    _i18n_labels = {
        "en": {
            "username_input": "Username",
            "password_input": "Password",
            "login_button": "Sign In",
            "switch_language_button": "languages",
        },
        "de": {
            "username_input": "Benutzername",
            "password_input": "Passwort",
            "login_button": "Anmelden",
            "switch_language_button": "languages",
        },
    }

    def set_content(self, *args, **kwargs):
        super().set_content(*args, **kwargs)

        self.current_language = self.page.locator("html").get_attribute("lang") or "en"

        self.username_input = self.page.get_by_role(
            "textbox", name=self._i18n_labels[self.current_language]["username_input"]
        )
        self.password_input = self.page.get_by_role(
            "textbox", name=self._i18n_labels[self.current_language]["password_input"]
        )
        self.login_button = self.page.get_by_role(
            "button", name=self._i18n_labels[self.current_language]["login_button"]
        )
        self.switch_language_button = self.page.get_by_role(
            "button",
            name=self._i18n_labels[self.current_language]["switch_language_button"],
        )

    def switch_language(self, name):
        self.switch_language_button.click()
        self.page.get_by_role("menuitem", name=name).click()
        # After changing the language,
        # the content must be resetted!
        self.set_content(page=self.page)

    def login(self, username, password):
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
