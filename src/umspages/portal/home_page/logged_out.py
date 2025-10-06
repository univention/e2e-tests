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

from ...common.base import expect
from .base import HomePage


class HomePageLoggedOut(HomePage):
    """
    This represents the portal homepage from the point-of-view of a user
    who has not yet logged in.
    """

    def set_content(self, *args, **kwargs):
        """
        The portal now has both SAML and OIDC login tiles:
        - "Login (Single sign-on)" - OIDC login (default)
        - "Login (SAML Single sign-on)" - SAML login
        """
        super().set_content(*args, **kwargs)

        # Specific login tiles
        self.oidc_login_tile = self.page.locator('xpath=//a[contains(@href, "univention/oidc")]')
        self.saml_login_tile = self.page.get_by_role("link", name="Login (SAML Single sign-on)")

        # Legacy SAML tile selector as fallback
        saml_legacy_tile = self.page.locator('xpath=//a[contains(@href, "univention/saml")]')
        self.saml_login_tile = self.saml_login_tile.or_(saml_legacy_tile)

        # Default login widget points to OIDC tile (default login method)
        # For backward compatibility, also match "Login (Single sign-on)" OIDC tile
        oidc_by_name = self.page.get_by_role("link", name="Login (Single sign-on)")
        self.login_widget = self.oidc_login_tile.or_(oidc_by_name)

    def navigate(self, cookies_accepted=False):
        self.page.goto("/")
        if not cookies_accepted:
            try:
                expect(self.cookie_dialog).to_be_visible()
            except AssertionError:
                pass
            else:
                self.accept_cookies()
        self.logout()
        # Normally, we don't use assertions inside the navigate() methods
        # Navigation roots are the exception, since they have to assure login state
        self.reveal_area(self.right_side_menu, self.header.hamburger_icon)
        expect(self.right_side_menu.login_button).to_be_visible()
        expect(self.right_side_menu.logout_button).to_be_hidden()
        self.hide_area(self.right_side_menu, self.header.hamburger_icon)

    def is_displayed(self):
        # Check that at least one login tile is visible (either OIDC or SAML)
        # Since both tiles may be present, we just verify OIDC tile by default
        expect(self.oidc_login_tile).to_be_visible()

    def click_login_widget(self):
        self.login_widget.click()

    def has_oidc_login_tile(self):
        """Check if OIDC login tile is visible"""
        try:
            expect(self.oidc_login_tile).to_be_visible()
            return True
        except AssertionError:
            return False

    def has_saml_login_tile(self):
        """Check if SAML login tile is visible"""
        try:
            expect(self.saml_login_tile).to_be_visible()
            return True
        except AssertionError:
            return False
