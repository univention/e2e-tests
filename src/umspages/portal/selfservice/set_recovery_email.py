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
import string

from ...common.base import BasePage
from ..home_page.logged_in import HomePageLoggedIn


class SetRecoveryEmailDialogPage(BasePage):
    def set_content(self, *args, **kwargs):
        super().set_content(*args, **kwargs)
        self.username_box = self.page.get_by_label("username *")
        self.password_box = self.page.get_by_test_id("password-box")
        self.next_button = self.page.get_by_role("button", name="Next")
        self.email_box = self.page.get_by_role("textbox", name="Email", exact=True)
        self.retype_email_box = self.page.get_by_role("textbox", name="Email (retype)")
        self.submit_button = self.page.get_by_role("button", name="Submit")

    def navigate(self, username, password):
        home_page_logged_in = HomePageLoggedIn(self.page)
        home_page_logged_in.navigate(username, password)
        home_page_logged_in.reveal_area(
            home_page_logged_in.right_side_menu,
            home_page_logged_in.header.hamburger_icon,
        )
        home_page_logged_in.right_side_menu.click_entry("User settings")
        home_page_logged_in.right_side_menu.click_sub_entry(
            re.compile("My password recovery options")
        )
        self.username_box.fill(username)
        self.password_box.fill(password)
        self.next_button.click()

    def set_recovery_email(self, email: string):
        self.email_box.fill(email)
        self.retype_email_box.fill(email)
        self.submit_button.click()
