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

from ....common.base import BasePagePart, expect


class Header(BasePagePart):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.account_menu_button = self.page_part_locator.get_by_role("button", name="admin")
        self.account_menu_dropdown = AccountMenuDropdown(self.page_part_locator.get_by_role("menu", name="admin"))

    def click_account_menu_button(self):
        self.account_menu_button.click()

    def logout(self):
        self.click_account_menu_button()
        expect(self.account_menu_dropdown).to_be_visible()
        self.account_menu_dropdown.click_sign_out_button()


class AccountMenuDropdown(BasePagePart):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sign_out_button = self.page_part_locator.get_by_role("menuitem", name="Sign out")

    def click_sign_out_button(self):
        self.sign_out_button.click()

    def check_its_there(self):
        expect(self.sign_out_button).to_be_visible()
