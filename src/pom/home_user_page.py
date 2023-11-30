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


from playwright.sync_api import Locator, Page

from pom.base_page import BasePage


class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.lang = page.locator("html").get_attribute("lang")
        self.title = page.locator("head").locator("title").inner_text()
        self.header =page.locator("#portal-header")

        # Right side header buttons
        self.search_icon = page.locator("#header-button-search")
        self.bell_icon = page.locator("#header-button-bell")
        self.menu_icon = page.locator("#header-button-menu")

        # Menu elements
        self.menu_logout_link = page.locator(
            '#portal-sidenavigation'
        ).locator('#loginButton')

        self.announcement_container = page.locator("#announcement-container")

    def get_announcements(self) -> list:
        if self.announcement_container.is_visible():
            announcements = self.announcement_container.locator('.announcement-message').all()
            return [m.inner_text() for m in announcements]
        return []


class AdminHomePage(HomePage):
    def __init__(self, page: Page):
        super().__init__(page)

        # Page elements
        self.user_widget = page.locator('.portal-tile__root-element').locator('[to*="udm:users/user"]')
        self.user_title = self.user_widget.locator('.portal-tile__name').inner_text()
        self.group_widget = page.locator('.portal-tile__root-element').locator('[to*="udm:groups/group"]')
        self.group_title = self.group_widget.locator('.portal-tile__name').inner_text()
        self.mailboxes_widget = page.locator('.portal-tile__root-element').locator(
            '[to*="udm:oxmail/functional_account"]')
        self.mailboxes_title = self.mailboxes_widget.locator('.portal-tile__name').inner_text()
        self.resources_widget = page.locator('.portal-tile__root-element').locator(
            '[to*="udm:oxresources/oxresources"]')
        self.resources_title = self.resources_widget.locator('.portal-tile__name').inner_text()
        self.announcements_widget = page.locator('.portal-tile__root-element').locator(
            '[to*="udm:portals/announcement"]')
        self.announcements_title = self.announcements_widget.locator('.portal-tile__name').inner_text()


class UserHomePage(HomePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.email_widget = page.locator('.portal-tile__root-element').locator('[to*="io.ox/mail"]')
        self.email_title = self.email_widget.locator('.portal-tile__name').inner_text()
        self.calendar_widget = page.locator('.portal-tile__root-element').locator('[to*="io.ox/calendar"]')
        self.calendar_title = self.calendar_widget.locator('.portal-tile__name').inner_text()
        self.contacts_widget = page.locator('.portal-tile__root-element').locator('[to*="io.ox/contacts"]')
        self.contacts_title = self.contacts_widget.locator('.portal-tile__name').inner_text()
        self.tasks_widget = page.locator('.portal-tile__root-element').locator('[to*="io.ox/tasks"]')
        self.tasks_title = self.tasks_widget.locator('.portal-tile__name').inner_text()
        self.files_widget = page.locator('.portal-tile__root-element').locator('[to*="apps/files"]')
        self.files_title = self.files_widget.locator('.portal-tile__name').inner_text()
        self.activity_widget = page.locator('.portal-tile__root-element').locator('[to*="apps/activity"]')
        self.activity_title = self.activity_widget.locator('.portal-tile__name').inner_text()
        self.folder_widget = page.locator('.portal-folder')
        self.folder_title = self.folder_widget.locator('.portal-folder__name').inner_text()
        self.projects_widget = page.locator('.portal-tile__root-element').locator('[aria-label="Projects New Tab"]')
        self.projects_title = self.projects_widget.locator('.portal-tile__name').inner_text()
        self.knowledge_widget = page.locator('.portal-tile__root-element').locator(
            '[aria-label="Knowledge New Tab"]')
        self.knowledge_title = self.knowledge_widget.locator('.portal-tile__name').inner_text()
        self.collaboration_widget = page.locator('.portal-tile__root-element').locator(
            '[aria-label="Collaboration New Tab"]')
        self.collaboration_title = self.collaboration_widget.locator('.portal-tile__name').inner_text()
        self.video_widget = page.locator('.portal-tile__root-element').locator(
            '[aria-label="Ad hoc videoconference New Tab"]')
        self.video_title = self.video_widget.locator('.portal-tile__name').inner_text()

