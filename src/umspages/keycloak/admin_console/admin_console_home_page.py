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
from ..admin_login_page import AdminLoginPage
from .common.admin_console_page import AdminConsolePage


class AdminConsoleHomePage(AdminConsolePage):
    def set_content(self, *args, **kwargs):
        super().set_content(*args, **kwargs)
        self.realm_selector = self.page.get_by_test_id("realmSelectorToggle")

    def navigate(self, username, password):
        # this page is the canonical navigation root for logged in pages, so using URL to navigate
        self.page.goto("/admin/master/console/")
        try:
            # Check if logged in
            expect(self.header.account_menu_dropdown).to_be_visible()
        except AssertionError:
            admin_login_page = AdminLoginPage(self.page)
            admin_login_page.navigate()
            admin_login_page.is_displayed()
            admin_login_page.login(username, password)

    def is_displayed(self):
        expect(self.realm_selector).to_be_visible()
