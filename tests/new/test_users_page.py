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

import pytest
from playwright.sync_api import expect

from pom.home_user_page import AdminHomePage, UserHomePage


@pytest.mark.devenv
@pytest.mark.gaia
class TestGaiaHomePage:
    def test_portal_user_home_page_design(
            self,
            portal_base_url: str,
            user_home_page: UserHomePage,
            localization: dict,
    ):
        page = user_home_page

        assert page.title == 'Sovereign Workplace'
        expect(page.search_icon).to_be_visible()
        expect(page.bell_icon).to_be_visible()
        expect(page.menu_icon).to_be_visible()
        expect(page.email_widget).to_be_visible()
        expect(page.calendar_widget).to_be_visible()
        expect(page.contacts_widget).to_be_visible()
        expect(page.tasks_widget).to_be_visible()
        expect(page.files_widget).to_be_visible()
        expect(page.activity_widget).to_be_visible()
        expect(page.folder_widget).to_be_visible()
        expect(page.projects_widget).to_be_visible()
        expect(page.knowledge_widget).to_be_visible()
        expect(page.collaboration_widget).to_be_visible()
        expect(page.video_widget).to_be_visible()

        page.menu_icon.click()
        expect(page.menu_logout_link).to_be_visible()

        # Check localization
        assert page.lang == localization.lang

        loc = localization.user_home_page

        assert page.menu_logout_link.inner_text() == loc.MENU_LOGOUT_TEXT
        assert page.email_title == loc.EMAIL_WIDGET_TITLE
        assert page.calendar_title == loc.CALENDAR_WIDGET_TITLE
        assert page.contacts_title == loc.CONTACTS_WIDGET_TITLE
        assert page.tasks_title == loc.TASKS_WIDGET_TITLE
        assert page.files_title == loc.FILES_WIDGET_TITLE
        assert page.activity_title == loc.ACTIVITY_WIDGET_TITLE
        assert page.folder_title == loc.FOLDER_WIDGET_TITLE
        assert page.projects_title == loc.PROJECTS_WIDGET_TITLE
        assert page.knowledge_title == loc.KNOWLEDGE_WIDGET_TITLE
        assert page.collaboration_title == loc.COLLABORATION_WIDGET_TITLE
        assert page.video_title == loc.VIDEO_WIDGET_TITLE

        # Check Logout
        page.menu_logout_link.click(timeout=3000)
        expect(page._page).to_have_url(portal_base_url + '/univention/portal/#/')

    def test_portal_admin_home_page_design(
            self,
            portal_base_url: str,
            admin_home_page: AdminHomePage,
            localization: dict,
    ):
        page = admin_home_page

        assert page.title == 'Sovereign Workplace'
        expect(page.search_icon).to_be_visible()
        expect(page.bell_icon).to_be_visible()
        expect(page.menu_icon).to_be_visible()

        expect(page.user_widget).to_be_visible()
        expect(page.group_widget).to_be_visible()
        expect(page.mailboxes_widget).to_be_visible()
        expect(page.resources_widget).to_be_visible()
        expect(page.announcements_widget).to_be_visible()

        page.menu_icon.click()
        expect(page.menu_logout_link).to_be_visible()

        # Check localization
        assert page.lang == localization.lang

        loc = localization.admin_home_page

        assert page.user_title == loc.USER_WIDGET_TITLE
        assert page.group_title == loc.GROUP_WIDGET_TITLE
        assert page.mailboxes_title == loc.MAILBOXES_WIDGET_TITLE
        assert page.resources_title == loc.RESOURVES_WIDGET_TITLE
        assert page.announcements_title == loc.ANNOUNCEMENTS_WIDGET_TITLE
        assert page.menu_logout_link.inner_text() == loc.MENU_LOGOUT_TEXT

        # Check Logout
        page.menu_logout_link.click(timeout=3000)
        expect(page._page).to_have_url(portal_base_url + '/univention/portal/#/')
