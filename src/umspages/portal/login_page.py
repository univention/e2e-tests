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
        self.username_input = self.page.locator("#username")
        self.password_input = self.page.locator("#password")
        # TODO: Using regular expression to target both UCS and SouvAP envs. Needs a better solution.
        self.login_button = self.page.get_by_role("button", name=re.compile("^(Login|Sign In|Anmelden)"))

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

    def login_and_ensure_success(self, username, password):
        with capture_response(self.page, self.authenticate_url_pattern) as response_info:
            self.login(username, password)
        self.assert_successful_login(response_info.value)

    login_with_retry = retrying_keycloak_login(login_and_ensure_success)

    def login(self, username, password):
        self.fill_username(username)
        self.fill_password(password)
        self.click_login_button()

    def assert_successful_login(self, response):
        """
        429 indicates that the brute-force detection was triggered
        400 indicates that the LDAP Server request from Keycloak failed.
        These failure scenarios can easily be reproduced
        by deleting all ldap-server-secondary pods.

        200 could mean success or that the username or password was wrong.
        To differentiate these cases, we check the response text.
        """
        assert (
            response.status != 429
        ), "Login failed, probably reached the brute-force detection limits of keycloak-extensions"
        assert response.status == 200, "Login failed, probably due to a failed LDAP Connection"
        response_text = response.text()
        assert (
            "Redirecting, please wait." in response_text
        ), "Login failed, probably due to a wrong username or password."

    def switch_language(self, name):
        # TODO: Always should set the "lang" attribute.
        # See https://git.knut.univention.de/univention/components/univention-portal/-/issues/708

        self.page.get_by_role("button", name="languages").click()
        self.page.get_by_role("menuitem", name=name).click()


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
