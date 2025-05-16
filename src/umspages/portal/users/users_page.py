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
from typing import Optional

from ...common.base import BasePage, BasePagePart, expect


class UCSUsersPage(BasePage):
    def set_content(self, *args, **kwargs):
        super().set_content(*args, **kwargs)
        # TODO: using an iFrame here might be different in the SouvAP env
        # and will likely break test_users_page.
        self.iframe = self.page.frame_locator('iframe[title="Users"]')
        self.add_user_dialog = AddUserDialog(self.iframe.locator(":scope"))
        self.add_user_button = self.iframe.get_by_role("button", name="Add")
        self.column_header_name = self.iframe.get_by_role("columnheader", name="Name")
        self.column_header_path = self.iframe.get_by_role("columnheader", name="Path")
        self.delete_button = self.iframe.get_by_role("button", name="Delete")
        self.delete_confirm_button = (
            self.iframe.get_by_role("dialog").filter(has_text="Delete objects").get_by_role("button", name="Delete")
        )

    def add_user(self, username: str, password: str):
        expect(self.add_user_button).to_be_visible(timeout=10000)
        self.add_user_button.click()
        self.add_user_dialog.add_user(username, password)
        expect(self.iframe.locator(f"[id*={username}]")).to_be_visible()

    def remove_user(self, username: str):
        self.iframe.locator(f"[id*={username}]").click()
        self.delete_button.click()
        self.delete_confirm_button.click()
        self.iframe.locator(f"[id*={username}]").wait_for(state="hidden")


class AddUserDialog(BasePagePart):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.container_indicator = self.page_part_locator.get_by_label("Container", exact=True)
        self.template = self.page_part_locator.get_by_label("User template")
        self.first_name = self.page_part_locator.get_by_role("textbox", name="First name")
        self.last_name = self.page_part_locator.get_by_role("textbox", name="Last name *")
        self.username = self.page_part_locator.get_by_role("textbox", name="User name *")
        self.next_button = self.page_part_locator.get_by_role("button", name="Next")
        self.invite_email = self.page_part_locator.get_by_role(
            "textbox", name="Mail address to which the invitation link is sent"
        )
        self.set_password_button = self.page_part_locator.get_by_label("Invite user via e-mail.")
        self.password_box = self.page_part_locator.get_by_role("textbox", name="Password *")
        self.retype_box = self.page_part_locator.get_by_role("textbox", name="Password (retype) *")
        self.submit_password_button = self.page_part_locator.get_by_role("button", name="Create user")

    def add_user(
        self,
        username: str,
        password: Optional[str] = None,
        invite_email: Optional[str] = None,
    ):
        assert password or invite_email, "Either password or invite_email has to be specified to create a user"

        if self.container_indicator.is_visible():
            self.container_indicator.fill(":/users")
            self.page_part_locator.get_by_text(re.compile("users$")).click()
        expect(self.template).to_be_visible()
        self.template.fill("selfserviceregistrationtemplate")
        self.next_button.click()
        self.first_name.fill(username)
        self.last_name.fill(username)
        self.username.fill(username)
        self.next_button.click()
        if password:
            self.password_box.fill(password)
            self.retype_box.fill(password)
        else:
            self.set_password_button.click()
            self.invite_email.fill(invite_email)

        self.submit_password_button.click()
        expect(self.page_part_locator.get_by_text(f'The user "{username}" has been created.')).to_be_visible()
        self.page_part_locator.press("Escape")
