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

from e2e.decorators import retrying_slow
from umspages.common.base import expect

from ..login_page import LoginPage
from .base import HomePage


class HomePageLoggedIn(HomePage):
    """This represents the logged in state of the portal's home page."""

    def set_content(self, *args, **kwargs):
        super().set_content(*args, **kwargs)
        self.umc_heading = self.page.get_by_text("Univention Management Console", exact=True)
        self.users_tile = self.page.get_by_role("link", name=re.compile("Users New Tab|Users iFrame"))
        self.announcements_tile = self.page.get_by_role("link", name=re.compile("Announcements New Tab"))

        self.mail_tile = self.page.get_by_role("link", name="E-Mail New Tab")
        self.calendar_tile = self.page.get_by_role("link", name="Calendar New Tab")
        self.contacts_tile = self.page.get_by_role("link", name="Contacts New Tab")
        self.tasks_tile = self.page.get_by_role("link", name="Tasks New Tab")

        self.files_tile = self.page.get_by_role("link", name="Files New Tab")
        self.activity_tile = self.page.get_by_role("link", name="Activity New Tab")
        self.new_files_folder_tile = self.page.get_by_role("button", name="Create new files Folder", exact=False)

        self.projects_tile = self.page.get_by_role("link", name="Projects New Tab")
        self.knowledge_tile = self.page.get_by_role("link", name="Knowledge New Tab")

        self.collaboration_tile = self.page.get_by_role("link", name="Collaboration New Tab")
        self.video_conference_tile = self.page.get_by_role("link", name="Ad hoc videoconference New Tab")

    def navigate(self, username, password):
        self.page.goto("/")

        # TODO: Calling "navigate" should ensure that we are logged in.
        # Detection of the login state either by checking the cookie or by
        # looking at an element.
        #
        # Since every test case has a fresh browser context, we do actually
        # know if we are logged in or not. This means that we could also remove
        # the login-on-demand here and keep navigate very simple, and then
        # instead demand that a test case states if it needs the login state or
        # something else.
        #
        # Triggering the login is something which actually should NOT be done
        # by the LoginPage, it does not know if which way the user wants to log
        # in. The portal page should have a way to say "login_via_menu.click()"
        # and then the LoginPage.login(username, password) can be called.

        @retrying_slow
        def login():
            login_page = LoginPage(self.page)
            login_page.navigate(cookies_accepted=True)
            login_page.is_displayed()
            login_page.login(username, password)
            self.page.wait_for_url("/univention/portal/**", timeout=500)

        login()

        @retrying_slow
        def assert_tiles():
            # TODO: We miss a proper way to find the element, a "data-testid"
            # would be helpful in this case.
            tiles = self.page.locator("a.portal-tile")
            try:
                expect(tiles.first).to_be_visible(timeout=500)
            except Exception:
                self.page.reload()
                raise

        assert_tiles()

    def is_displayed(self):
        # TODO: There seems to be nothing that's necessarily common between the UCS and SouvAP envs
        # We resort to checking nothing here.
        pass

    def click_users_tile(self):
        return self.get_new_tab(self.users_tile)

    def click_announcements_tile(self):
        return self.get_new_tab(self.announcements_tile)
