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


from ...common.base import BasePage, expect
from ..home_page.logged_in import HomePageLoggedIn


class ManageProfileDialogPage(BasePage):
    def set_content(self, *args, **kwargs):
        super().set_content(*args, **kwargs)
        self.telephone_box = (
            self.page.locator('[data-test="form-element"]')
            .filter(has_text="Telephone number")
            .locator('input[type="text"]')
            .first
        )
        self.title_box = self.page.get_by_role("textbox", name="Title")
        self.first_name_box = self.page.get_by_role("textbox", name="First name *")
        self.last_name_box = self.page.get_by_role("textbox", name="Last name *")
        self.display_name_box = self.page.get_by_role("textbox", name="Display name")
        self.initials_box = self.page.get_by_role("textbox", name="Initials")
        self.organisation_box = self.page.get_by_role("textbox", name="Organisation")
        self.street_box = self.page.get_by_role("textbox", name="Street")
        self.postal_code_box = self.page.get_by_role("textbox", name="Postal code")
        self.city_box = self.page.get_by_role("textbox", name="City")
        self.save_button = self.page.get_by_role("button", name="Save")
        self.close_button = self.page.get_by_role("button", name="Close")
        self.upload_image = self.page.get_by_role("button", name="Upload")

    def navigate(self, username, password):
        home_page_logged_in = HomePageLoggedIn(self.page)
        home_page_logged_in.navigate(username, password)

        self.page.reload()
        home_page_logged_in.reveal_area(
            home_page_logged_in.right_side_menu,
            home_page_logged_in.header.hamburger_icon,
        )
        home_page_logged_in.right_side_menu.menu_entry("User settings").click(timeout=5000)
        home_page_logged_in.right_side_menu.click_sub_entry("My Profile")

    def change_telephone(self, description):
        self.telephone_box.fill(description)
        self.save_button.click()
        expect(self.save_button).to_be_hidden(timeout=10000)

    def change_profile_picture(self):
        with self.page.expect_file_chooser() as fc_info:
            self.upload_image.click()
        file_chooser = fc_info.value
        file_chooser.set_files("./src/umspages/portal/selfservice/resources/NUBUS_ICON.png")
        self.save_button.click()
        expect(self.save_button).to_be_hidden(timeout=10000)
