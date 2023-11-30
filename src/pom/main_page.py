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


from playwright.sync_api import Page

from pom.base_page import BasePage


class MainPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.lang = page.locator("html").get_attribute("lang")
        self.title = page.locator("head").locator("title").inner_text()
        self.header = page.locator("#portal-header").locator("h1").inner_text()

        self.cookie_dialog = page.locator(".cookie-banner-modal")
        self.cookie_dialog_accept_button = self.cookie_dialog.get_by_role("button")

        self.category_1 = page.locator('div[class="portal-category"]').locator("nth=0")
        self.category_2 = page.locator('div[class="portal-category"]').locator("nth=1")

        # TODO fix it: 'Login' text is locale dependent
        self.login_widget = self.category_1.locator(
            'span[class="portal-tile__name"]'
        ).get_by_text("Login")
        self.login_saml_widget = self.category_2.locator(
            'span[class="portal-tile__name"]'
        ).get_by_text("Login")

        # Header buttons
        self.search = page.locator("#header-button-search")
        self.bell = page.locator("#header-button-bell")
        self.menu_icon = page.locator("#header-button-menu")
        self.menu_login_button = page.locator("#portal-sidenavigation").locator(
            "#loginButton"
        )

        self.announcement_container = page.locator("#announcement-container")

    def accept_cookie(self):
        if self.cookie_dialog.is_visible():
            self.cookie_dialog_accept_button.click()

    def get_announcements(self) -> list:
        if self.announcement_container.is_visible():
            announcements = self.announcement_container.locator('.announcement-message').all()
            return [m.inner_text() for m in announcements]
        return []

