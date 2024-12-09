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

from typing import Optional

from ...common.base import BasePage, expect


class UCSGroupsPage(BasePage):
    def set_content(self, *args, **kwargs):
        super().set_content(*args, **kwargs)
        self.iframe = self.page.frame_locator('iframe[title="Groups"]')

        # Buttons
        self.add_button = self.iframe.get_by_role("button", name="Add")
        self.edit_button = self.iframe.get_by_role("button", name="Edit")
        self.more_button = self.iframe.get_by_label("more", exact=True)
        self.delete_button = self.iframe.get_by_role("button", name="Delete")
        self.delete_confirm_button = (
            self.iframe.get_by_role("dialog").filter(has_text="Delete objects").get_by_role("button", name="Delete")
        )
        # Dialogs
        self.edit_dialog = GroupDialog(self.iframe)

        # Table
        self.column_header_name = self.iframe.get_by_role("columnheader", name="Name")
        self.column_header_path = self.iframe.get_by_role("columnheader", name="Path")

    def add_group(self, name: str, description: Optional[str] = None):
        expect(self.add_button).to_be_visible(timeout=10000)
        self.add_button.click()
        self.edit_dialog.create_group(name, group_description=description)
        expect(self.iframe.get_by_role("gridcell", name=name)).to_be_visible()

    def edit_group(self, name: str, new_name: Optional[str] = None, new_description: Optional[str] = None):
        expect(self.add_button).to_be_visible(timeout=10000)
        group_cell = self.iframe.get_by_role("gridcell", name=name)
        expect(group_cell).to_be_visible()
        group_cell.click()
        self.edit_button.click()
        self.edit_dialog.edit_group(new_name or name, new_description=new_description)
        expect(self.iframe.get_by_role("gridcell", name=new_name or name)).to_be_visible()

    def remove_group(self, name: str):
        expect(self.add_button).to_be_visible(timeout=10000)
        group_cell = self.iframe.get_by_role("gridcell", name=name)
        expect(group_cell).to_be_visible()
        group_cell.click()
        self.delete_button.click()
        self.delete_confirm_button.click()
        group_cell.wait_for(state="hidden")


class GroupDialog(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Inputs
        self.group_name_input = self.page.get_by_label("Name *")
        self.group_description_input = self.page.get_by_label("Description")

        # Buttons
        self.create_button = self.page.get_by_label("Create group")
        self.save_button = self.page.get_by_label("Save")

    def fill_group_fields(self, group_name: str, group_description: Optional[str] = None):
        self.group_name_input.fill(group_name)
        if group_description:
            self.group_description_input.fill(group_description)

    def create_group(self, group_name: str, group_description: Optional[str] = None):
        self.fill_group_fields(group_name, group_description=group_description)
        self.create_button.click()

    def edit_group(self, group_name: str, new_description: Optional[str] = None):
        self.fill_group_fields(group_name, group_description=new_description)
        self.save_button.click()
