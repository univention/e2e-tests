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

from ...common.base import BasePagePart


class RightSideMenu(BasePagePart):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logout_button = self.page_part_locator.get_by_role("button", name="Logout")
        self.login_button = self.page_part_locator.get_by_role("button", name="Login")

    def click_logout_button(self):
        self.logout_button.click()

    def click_login_button(self):
        self.login_button.click()

    def click_entry(self, name):
        self.menu_entry(name).click()

    def menu_entry(self, name):
        return self.page_part_locator.get_by_role("button", name=name)

    def click_sub_entry(self, name):
        self.sub_menu_entry(name).click()

    def sub_menu_entry(self, name):
        return self.page_part_locator.get_by_role("link", name=name)
