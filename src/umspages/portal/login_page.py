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
import time
from dataclasses import dataclass

import pyotp

from e2e.decorators import retrying_keycloak_login

from ..common.base import expect
from .common.portal_page import PortalPage
from .home_page.logged_out import HomePageLoggedOut


@dataclass
class TotpSetup:
    secret: str | None = None
    last_token_used: str | None = None


# TODO: Split into UCSLoginPage and KeycloakLoginPage
class LoginPage(PortalPage):
    def set_content(self, *args, **kwargs):
        super().set_content(*args, **kwargs)
        # TODO: Using regular expr to target different langs in SouvAP env. Needs better solution.
        # In headed mode, default language is English. In headless mode, it is Deutsch.
        self.username_input = self.page.get_by_role("textbox", name="Username")
        self.password_input = self.page.get_by_role("textbox", name="Password")
        self.totp_input = self.page.get_by_role("textbox", name="One-time code")

        self.totp_unable_to_scan = self.page.get_by_role("link", name="Unable to scan?")

        self.totp_secret_key = self.page.locator("id=kc-totp-secret-key")
        # TODO: Using regular expression to target both UCS and SouvAP envs. Needs a better solution.
        self.login_button = self.page.get_by_role("button", name=re.compile("^(Login|Sign In)"))
        self.submit_button = self.page.get_by_role("button", name="Submit")
        # Keycloak login specific

        # TODO: Missing role in the sources
        # Should use "page.get_by_role("dialog", ...)" instead
        self.cookie_dialog = self.page.locator(".cookie-banner .dialog")
        self.forgot_password_link = self.page.get_by_role("link", name="Forgot password")

        # Ad-hoc provisioning options
        self.ad_hoc_provisioning_button = self.page.locator("#kc-social-providers").get_by_role(
            "link", name="OIDC test"
        )

    def navigate(self, cookies_accepted=False):
        """Navigate to login page using default (OIDC) login method"""
        home_page = HomePageLoggedOut(self.page)
        home_page.navigate(cookies_accepted=cookies_accepted)
        home_page.is_displayed()
        self.reveal_area(self.right_side_menu, self.header.hamburger_icon)
        expect(self.right_side_menu.login_button).to_be_visible()
        expect(self.right_side_menu.logout_button).to_be_hidden()
        self.right_side_menu.click_login_button()

    def navigate_oidc(self, cookies_accepted=False):
        """Navigate to login page using OIDC login tile specifically"""
        home_page = HomePageLoggedOut(self.page)
        home_page.navigate(cookies_accepted=cookies_accepted)
        home_page.is_displayed()
        home_page.oidc_login_tile.click()

    def navigate_saml(self):
        """Navigate to login page using SAML login tile specifically"""
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

    def fill_totp(self, totp):
        self.totp_input.fill(totp)

    def click_login_button(self):
        self.login_button.click()

    def login_and_ensure_success(self, username, password, totp_setup: TotpSetup | None = None):
        """
        Perform login without response validation.

        Note: Response validation was removed because the response capture mechanism
        is unreliable for OIDC flows - it captures the final response in the redirect
        chain (200 from portal) instead of the immediate Keycloak response (302).
        Navigation-based validation in the calling code is more reliable.
        """
        self.login(username, password, totp_setup)

    login_with_retry = retrying_keycloak_login(login_and_ensure_success)

    def login(self, username, password, totp_setup: TotpSetup | None = None):
        """
        Perform login with the given username and password.

        This method supports setting up and logging in with TOTP.

        For TOTP this function works in two different modes.

        If `totp_secret` is passed, it's assumed that the user who logs in has TOTP already configured
        and will be prompted to enter the TOTP code after submitting username and password.
        `totp_secret` is the Base32 hex string without spaces.
        It is passed to `pyotp` and a one time code is generated.

        If an instance of `TotpSetup` with the attribute `secret` set to `None` is passed to the `totp_setup` argument
        it is assumed that the user will be prompted to setup TOTP after submitting username and password.
        The TOTP secret key is then stored in the `secret` attribute of the `TotpSetup` class.

        You can not set both `totp_secret` and `totp_setup` at the same time.
        """
        self.fill_username(username)
        self.fill_password(password)
        self.click_login_button()

        if totp_setup and not totp_setup.secret:
            self.totp_setup(totp_setup)
        elif totp_setup:
            totp = pyotp.TOTP(totp_setup.secret)
            token = totp.now()
            while totp_setup.last_token_used is not None and token == totp_setup.last_token_used:
                time.sleep(1)
                token = totp.now()
            self.fill_totp(token)
            self.click_login_button()

    def totp_setup(self, totp_setup: TotpSetup):
        self.totp_unable_to_scan.click()
        expect(self.totp_secret_key).to_be_visible()

        key = self.totp_secret_key.inner_text().strip().replace(" ", "")
        totp_setup.secret = key
        token = pyotp.TOTP(key).now()
        self.fill_totp(token)
        totp_setup.last_token_used = token
        self.submit_button.click()
