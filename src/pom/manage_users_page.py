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


class ManageUsersPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.add_user_button = page.locator('[role="button"]:visible', has_text='Add')

    def get_users(self) -> list:
        return []

    def add_user(self, template: str, user: dict):
        self.add_user_button.click()

        # select user template
        frame = self._page.locator('[role="tabpanel"]').and_(self._page.locator('[aria-label="Add a new user."]'))
        # down_button = frame.locator('.umcTextBox__downArrowButton:visible')
        # down_button.click()
        # item = self._page.locator('.dijitMenuItem[item="1"]', has_text=template)
        # item.click()
        frame.locator('.umcPageFooterRight').locator(
            '[role="button"]:visible',
            has_text='Next'
        ).click()

        # set user parameters
        title = self._page.locator('input[name="title"]:visible')
        first_name = self._page.locator('input[name="firstname"]:visible')
        last_name = self._page.locator('input[name="lastname"]:visible')
        user_name = self._page.locator('input[name="username"]:visible')
        title.fill(user['title'])
        first_name.fill(user['first_name'])
        last_name.fill(user['last_name'])
        user_name.fill(user['user_name'])
        # mail_down_button = self._page.locator('.umcTextBox__downArrowButton:visible')
        # mail_down_button.click()
        # item = self._page.locator('#umc_widgets_MailBox_2_popup0[item="0"]')
        # item.click()
        self._page.locator('.umcPageFooterRight').locator(
            '[role="button"]:visible',
            has_text='Next'
        ).click()

        # set user password
        invite_checkbox = self._page.locator('text=Invite')
        invite_checkbox.click()
        password_1 = self._page.locator('input[name="password_1"]:visible')
        password_2 = self._page.locator('input[name="password_2"]:visible')
        password_1.fill(user['password'])
        password_2.fill(user['password'])
        self._page.locator('.umcPageFooterRight').locator(
            '[role="button"]:visible',
            has_text='Create user'
        ).click()
