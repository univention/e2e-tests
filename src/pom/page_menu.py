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

from pom.base_page import BasePage


class ToolbarMenu:
    def __init__(self, page: BasePage):
        self._menu = page._page.locator('.portal-sidenavigation__menu[role="toolbar"]')

        '''
         self.menu_language_button = self.page.locator("#portal-sidenavigation").locator(
            ".portal-sidenavigation__menu-item", has_text=" Change Language "
        )
        self.menu_privacy_button = self.page.locator("#portal-sidenavigation").locator(
            'a[target="ext_privacystatement"]'
        )
        self.menu_legalnotice_button = self.page.locator(
            "#portal-sidenavigation"
        ).locator('a[target="ext_legalnotice"]')
        '''


class MainToolbarMenu(ToolbarMenu):
    def __init__(self, page: BasePage):
        super().__init__(page)

        items = self._menu.locator('.portal-sidenavigation__menu-item')
        self.language_button = items.locator("nth=0")
        self.privacy_button = items.locator("nth=1")
        self.legalnotice_button = items.locator("nth=2")


class AdminToolbarMenu(ToolbarMenu):
    def __init__(self, page: BasePage):
        super().__init__(page)

        items = self._menu.locator('.portal-sidenavigation__menu-item')
        self.settings_button = items.locator("nth=0")
        self.language_button = items.locator("nth=1")
        self.privacy_button = items.locator("nth=2")
        self.legalnotice_button = items.locator("nth=3")


class UserToolbarMenu(ToolbarMenu):
    def __init__(self, page: BasePage):
        super().__init__(page)

        items = self._menu.locator('.portal-sidenavigation__menu-item')
        self.settings_button = items.locator("nth=0")
        self.language_button = items.locator("nth=1")
        self.privacy_button = items.locator("nth=2")
        self.legalnotice_button = items.locator("nth=3")


class DevenvMainToolbarMenu(ToolbarMenu):
    def __init__(self, page: BasePage):
        super().__init__(page)

        items = self._menu.locator('.portal - sidenavigation__menu-item')
        self.privacy_button = items.locator("nth=0")
        self.legalnotice_button = items.locator("nth=1")
