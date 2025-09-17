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
from contextlib import contextmanager

from e2e.decorators import retrying_keycloak_login

from ..common.base import expect
from .common.portal_page import PortalPage
from .home_page.logged_out import HomePageLoggedOut


# TODO: Split into UCSLoginPage and KeycloakLoginPage
class LoginPage(PortalPage):
    authenticate_url_pattern = re.compile(
        r".*/realms/"
        # realm name, typically "nubus" or "opendesk"
        r".*?"
        r"/login-actions/authenticate"
    )

    def set_content(self, *args, **kwargs):
        super().set_content(*args, **kwargs)
        # TODO: Using regular expr to target different langs in SouvAP env. Needs better solution.
        # In headed mode, default language is English. In headless mode, it is Deutsch.
        self.username_input = self.page.get_by_role("textbox", name="Username")
        self.password_input = self.page.get_by_role("textbox", name="Password")
        # TODO: Using regular expression to target both UCS and SouvAP envs. Needs a better solution.
        self.login_button = self.page.get_by_role("button", name=re.compile("^(Login|Sign In)"))
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

    def click_login_button(self):
        self.login_button.click()

    def login_and_ensure_success(self, username, password):
        with capture_response(self.page, self.authenticate_url_pattern) as response_info:
            self.login(username, password)

        # Wait for navigation away from login-actions page
        # The login might return an intermediate page that needs client-side processing
        try:
            # Wait for navigation away from login-actions URLs (max 10 seconds)
            self.page.wait_for_url(lambda url: "login-actions" not in url, timeout=10000)
        except:
            # If we're still on login-actions page, try refreshing as suggested
            current_url = self.page.url
            if "login-actions/authenticate" in current_url:
                self.page.reload()
                # Wait again for navigation after refresh
                try:
                    self.page.wait_for_url(lambda url: "login-actions" not in url, timeout=10000)
                except:
                    # Still stuck - this indicates a real login failure
                    pass

        # Check where we ended up and redirect to portal if needed
        current_url = self.page.url
        if "/univention/management" in current_url:
            # We were redirected to management instead of portal - navigate to portal manually
            from urllib.parse import urlparse

            parsed_url = urlparse(current_url)
            portal_url = f"{parsed_url.scheme}://{parsed_url.netloc}/univention/portal/"
            self.page.goto(portal_url)

        self.assert_successful_login(response_info.value)

    login_with_retry = retrying_keycloak_login(login_and_ensure_success)

    def login(self, username, password):
        self.fill_username(username)
        self.fill_password(password)
        self.click_login_button()

    def assert_successful_login(self, response):
        """
        Check if login was successful by examining both the response and final page state.

        429 indicates that the brute-force detection was triggered
        400 indicates that the LDAP Server request from Keycloak failed.

        For 200 responses, we need to check if we successfully navigated away from
        the login-actions page, as Keycloak may return intermediate pages that
        require client-side processing.
        """
        assert (
            response.status != 429
        ), "Login failed, probably reached the brute-force detection limits of keycloak-extensions"

        # Check final page state - the most reliable indicator of success
        current_url = self.page.url

        # If we're no longer on a login-actions page, login likely succeeded
        if "login-actions" not in current_url:
            return  # Success - we've navigated away from the auth page

        # If we're still on login-actions page, check for specific error indicators
        if response.status == 200:
            response_text = response.text()
            error_indicators = [
                "invalid_user_credentials",  # Keycloak error
                "Account is disabled",  # Account disabled
                "Login failed",  # Generic login error
                "Username or email",  # Back on login form
            ]
            for error_msg in error_indicators:
                if error_msg in response_text:
                    assert False, f"Login failed - found error indicator '{error_msg}' in response"

            # If no specific error found but still on login-actions page, it might be a timeout or processing issue
            assert False, f"Login appears to have failed - still on login-actions page: {current_url}"
        else:
            # Any non-200 status is a failure
            assert False, f"Login failed with status code {response.status}"


@contextmanager
def capture_response(page, pattern):
    """
    Captures the response body as a `str` for the given `pattern`.

    This does use `Page.route` to intercept the request, so that the response
    text can be extracted. Usually this would be done with
    `Page.expect_response` and `Response.finished` to wait until the body is
    available. For pages which trigger a redirect from a ``<script>`` block
    this does lead to errors being logged which are misleading when debugging a
    failed test.

    In comparison to `Page.expect_response` this implementation is very naive.
    It does not register any handlers around events of the `Page` being closed.
    This difference does seem to prevent the logging issue.

    The main use-case so far has been the `LoginPage`.
    """
    response_value = ResponseInfo()

    def handle_route(request):
        response = request.fetch()
        response_value.value = response
        request.fulfill(response=response)

    page.route(pattern, handle_route)
    try:
        yield response_value
    finally:
        page.unroute(pattern, handle_route)


class ResponseInfo:
    value = None
