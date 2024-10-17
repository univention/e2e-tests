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

    def click(self):
        self.page_part_locator.locator("#header-button-menu").click()

    def get_all_sidebar_entries_text(self) -> dict[str, list[str]]:
        """
        Retrieves all sidebar entries and their sub-entries.

        Returns:
            dict[str, list[str]]: Dictionary mapping main entries to lists of their sub-entries

        Raises:
            TimeoutError: If elements cannot be found within timeout period
            PlaywrightError: If DOM manipulation fails
        """
        sidebar_entries: dict[str, list[str]] = {}

        try:
            main_entries = self.page_part_locator.locator(".menu-item").all()

            for entry in main_entries:
                entry_text = entry.inner_text().split("\n")[0]
                sidebar_entries[entry_text] = []

                # Safely click and gather sub-entries
                try:
                    entry.click()
                    sub_entries = self.page_part_locator.locator(".menu-item").all()
                    if sub_entries:
                        sub_entries.pop(0)  # Remove the parent entry
                        for sub_entry in sub_entries:
                            sub_text = sub_entry.inner_text().split("\n")[0]
                            sidebar_entries[entry_text].append(sub_text)

                    # Close the sub-menu
                    self.page_part_locator.locator(".portal-sidenavigation__menu-subItem--parent").click()

                except Exception as e:
                    print(f"Failed to process sub-entries for {entry_text}: {str(e)}")
                    continue

            return sidebar_entries

        except Exception as e:
            print(f"Failed to retrieve sidebar entries: {str(e)}")
            raise
