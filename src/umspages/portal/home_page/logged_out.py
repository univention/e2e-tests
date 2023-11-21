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
        The saml login tile is often renamed from "Login (Single sign-on)" to "Login"
        This means that login_widget can be plain ucs login or saml login
        while saml_login_tile is always the saml tile, no matter the name.
        """
        super().set_content(*args, **kwargs)

        # It is perfectly fine that the portal is configured to have multiple
        # login tiles. By default we should use the first one. If a specific
        # one is needed, then attributes like `saml_login_tile` should be used.
        self.login_widget = self.page.get_by_role("link", name="Login Same tab").first
        self.saml_login_tile = self.page.locator('xpath=//a[contains(@href, "univention/saml")]')

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
        expect(self.login_widget).to_be_visible()

    def click_login_widget(self):
        self.login_widget.click()
