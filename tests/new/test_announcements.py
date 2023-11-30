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

from attrdict import AttrDict
from pom.home_user_page import AdminHomePage, UserHomePage
from pom.main_page import MainPage
from pom.manage_announcement_page import ManageAnnouncementsPage
from pom.udm import UDMSession

announcement_1 = AttrDict(
    properties=AttrDict(
        name='a4feb550-02b5-4805-9812-939529b44138',
        allowedGroups=[],
        isSticky=False,
        needsConfirmation=False,
        objectFlag=[],
        severity='info',
        title={'en_US': 'E2E Test Announcement Title'},
        message={'en_US': 'a4feb550-02b5-4805-9812-939529b44138'},
        visibleFrom=None,
        visibleUntil=None,
    ),
    position='cn=announcement,cn=portals,cn=univention,dc=univention-organization,dc=intranet',
)

announcement_2 = AttrDict(
    properties=AttrDict(
        name='b8f63fea-b490-4431-b7e1-5a2152417e57',
        allowedGroups=[],
        isSticky=False,
        needsConfirmation=False,
        objectFlag=[],
        severity='warn',
        title={'en_US': 'E2E Test Announcement Title'},
        message={'en_US': 'b8f63fea-b490-4431-b7e1-5a2152417e57'},
        visibleFrom=None,
        visibleUntil=None,
    ),
    position='cn=announcement,cn=portals,cn=univention,dc=univention-organization,dc=intranet',
)

announcement_3 = AttrDict(
    properties=AttrDict(
        name='cb9d83e5-f6c6-4050-9586-31bff3b2fb2e',
        allowedGroups=[],
        isSticky=True,
        needsConfirmation=True,
        objectFlag=[],
        severity='danger',
        title={'en_US': 'E2E Test Announcement Title'},
        message={'en_US': 'cb9d83e5-f6c6-4050-9586-31bff3b2fb2e'},
        visibleFrom=None,
        visibleUntil=None,
    ),
    position='cn=announcement,cn=portals,cn=univention,dc=univention-organization,dc=intranet',
)

fake_announcements = [
    announcement_1,
    announcement_2,
    announcement_3
]

@pytest.mark.gaia
@pytest.mark.devenv
class TestUdmApiAnnouncements:
    @pytest.mark.dependency()
    def test_udm_api_add_announcements(
            self,
            udm_session: UDMSession,
    ):
        for a in fake_announcements:
            assert udm_session.check_announcement_exists(a) is False
            udm_session.create_announcement(a)
            assert udm_session.check_announcement_exists(a) is True

    @pytest.mark.dependency(
        depends=[
            'TestUdmApiAnnouncements::test_udm_api_add_announcements'
        ]
    )
    def test_udm_api_remove_announcements(
            self,
            udm_session: UDMSession,
    ):
        for a in fake_announcements:
            assert udm_session.check_announcement_exists(a) is True
            udm_session.remove_announcement(a)
            assert udm_session.check_announcement_exists(a) is False


@pytest.mark.gaia
@pytest.mark.devenv
class TestWebAnnouncements:
    @pytest.mark.dependency()
    def test_web_check_announcements(
            self,
            main_page: MainPage,
    ):
        # Check that test announcement doesn't exist
        announcements = main_page.get_announcements()
        for a in fake_announcements:
            assert a['properties']['name'] not in announcements

    @pytest.mark.dependency(
        depends=[
            'TestWebAnnouncements::test_web_check_announcements'
        ]
    )
    def test_web_add_announcements(
            self,
            admin_home_page: AdminHomePage,
    ):
        page = admin_home_page

        # Create announcements
        for a in fake_announcements:
            with page._page.expect_popup() as popup_info:
                page.announcements_widget.click()
                popup_info.value.wait_for_load_state()
                a_page = ManageAnnouncementsPage(popup_info.value)
                a_page.add_announcement(a)
                assert a_page.is_announcement_on_page(a)
                a_page._page.close()

    @pytest.mark.dependency(
        depends=[
            'TestWebAnnouncements::test_web_add_announcements'
        ]
    )
    def test_main_page_announcements_exist(
            self,
            main_page: MainPage,
    ):
        announcements = main_page.get_announcements()
        for a in fake_announcements:
            assert a['properties']['name'] in announcements

    @pytest.mark.dependency(
        depends=[
            'TestWebAnnouncements::test_main_page_announcements_exist'
        ]
    )
    def test_user_page_announcements_exist(
            self,
            user_home_page: UserHomePage,
    ):
        announcements = user_home_page.get_announcements()
        for a in fake_announcements:
            assert a['properties']['name'] in announcements

    @pytest.mark.dependency(
        depends=[
            'TestWebAnnouncements::test_user_page_announcements_exist'
        ]
    )
    def test_web_remove_announcements(
            self,
            admin_home_page: AdminHomePage,
    ):
        page = admin_home_page
        with page._page.expect_popup() as popup_info:
            page.announcements_widget.click()
            popup_info.value.wait_for_load_state()
            a_page = ManageAnnouncementsPage(popup_info.value)
            for a in fake_announcements:
                a_page.remove_announcement(a)
                assert not a_page.is_announcement_on_page(a)
            a_page._page.close()

    @pytest.mark.dependency(
        depends=[
            'TestWebAnnouncements::test_web_remove_announcements'
        ]
    )
    def test_main_page_announcements_doesnt_exist(
            self,
            main_page: MainPage,
    ):
        announcements = main_page.get_announcements()
        for a in fake_announcements:
            assert a['properties']['name'] not in announcements

    @pytest.mark.dependency(
        depends=[
            'TestWebAnnouncements::test_main_page_announcements_doesnt_exist'
        ]
    )
    def test_user_page_announcements_doesnt_exist(
            self,
            user_home_page: UserHomePage,
    ):
        announcements = user_home_page.get_announcements()
        for a in fake_announcements:
            assert a['properties']['name'] not in announcements
