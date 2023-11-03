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

from ...common.base import BasePage  # type: ignore
from ..home_page.logged_in import HomePageLoggedIn


class ChangePasswordDialogPage(BasePage):
    def set_content(self, *args, **kwargs):
        super().set_content(*args, **kwargs)
        self.old_password_box = self.page.get_by_test_id(
            "password-box"
        )
        self.new_password_box = self.page.get_by_test_id(
            "new-password-box"
        )
        self.retype_password_box = self.page.get_by_test_id(
            "retype-password-box"
        )
        self.submit_button = self.page.get_by_role(
            "button",
            name="Change password"
        )

    def navigate(self, username, password):
        home_page_logged_in = HomePageLoggedIn(self.page)
        home_page_logged_in.navigate(username, password)
        home_page_logged_in.reveal_area(
            home_page_logged_in.right_side_menu,
            home_page_logged_in.header.hamburger_icon,
        )
        home_page_logged_in.right_side_menu.click_entry("User settings")
        # TODO: Using regular expression to target both UCS
        #  and SouvAP envs. Needs a better solution.
        home_page_logged_in.right_side_menu.click_sub_entry(
            re.compile("Change your password|Update my password")
        )

    def change_password(self, old_password: str, new_password: str):
        self.old_password_box.fill(old_password)
        self.new_password_box.fill(new_password)
        self.retype_password_box.fill(new_password)
        self.submit_button.click()
