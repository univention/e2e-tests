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

from ...common.base import expect
from .base import HomePage
from ..login_page import LoginPage


class HomePageLoggedIn(HomePage):
    """This represents the logged in state of the portal's home page."""

    def set_content(self, *args, **kwargs):
        super().set_content(*args, **kwargs)
        self.umc_heading = self.page.get_by_text("Univention Management Console", exact=True)
        self.users_tile = self.page.get_by_role("link", name=re.compile("User New Tab|Users iFrame"))

        self.mail_tile = self.page.get_by_role("link", name="E-Mail New Tab")
        self.calendar_tile = self.page.get_by_role("link", name="Calendar New Tab")
        self.contacts_tile = self.page.get_by_role("link", name="Contacts New Tab")
        self.tasks_tile = self.page.get_by_role("link", name="Tasks New Tab")

        self.files_tile = self.page.get_by_role("link", name="Files New Tab")
        self.activity_tile = self.page.get_by_role("link", name="Activity New Tab")
        self.new_files_folder_tile = self.page.get_by_role("button", name="Create new files Folder", exact=False)

        self.projects_tile = self.page.get_by_role("link", name="Projects New Tab")
        self.knowledge_tile = self.page.get_by_role("link",name="Knowledge New Tab")

        self.collaboration_tile = self.page.get_by_role("link",name="Collaboration New Tab")
        self.video_conference_tile = self.page.get_by_role("link", name="Ad hoc videoconference New Tab")

    def navigate(self, username, password):
        self.page.goto("/")
        try:
            expect(self.cookie_dialog).to_be_visible()
        except AssertionError:
            pass
        else:
            self.accept_cookies()
        self.reveal_area(self.right_side_menu, self.header.hamburger_icon)
        try:
            expect(self.right_side_menu.login_button).to_be_visible()
        except AssertionError:
            expect(self.right_side_menu.logout_button).to_be_visible()
        else:
            login_page = LoginPage(self.page)
            login_page.navigate(cookies_accepted=True)
            login_page.is_displayed()
            login_page.login(username, password)
            self.reveal_area(self.right_side_menu, self.header.hamburger_icon)
            expect(self.right_side_menu.logout_button).to_be_visible()
            expect(self.right_side_menu.login_button).to_be_hidden()
        finally:
            self.hide_area(self.right_side_menu, self.header.hamburger_icon)

    def is_displayed(self):
        # TODO: There seems to be nothing that's necessarily common between the UCS and SouvAP envs
        # We resort to checking nothing here.
        pass

    def click_users_tile(self):
        self.users_tile.click()
