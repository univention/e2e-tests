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


class WelcomePage(BasePage):
    def set_content(self, *args, **kwargs):
        super().set_content(*args, **kwargs)
        self.administrator_console_link = self.page.get_by_role(
            "link", name="Administration Console")

    def click_administrator_console_link(self):
        self.administrator_console_link.click()

    def navigate(self):
        self.page.goto("/admin/master/console/")
        account_menu_button = self.page.get_by_role("button", name="admin")
        try:
            # Check if logged in
            expect(account_menu_button).to_be_visible()
        except AssertionError:
            self.page.goto("/")
        else:
            account_menu_button.click()
            account_menu_dropdown = self.page.get_by_role(
                "button", name="admin")
            expect(account_menu_dropdown).to_be_visible()
            account_menu_dropdown.get_by_role(
                "menuitem", name="Sign out").click()
            self.page.goto("/admin/master/console/")
            expect(account_menu_button).to_be_hidden()
            self.page.goto("/")

    def is_displayed(self):
        expect(self.administrator_console_link).to_be_visible()
