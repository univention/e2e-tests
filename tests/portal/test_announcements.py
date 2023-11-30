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

from umspages.common.base import expect
from umspages.portal.announcements.announcements_page import AnnouncementsPage
from umspages.portal.home_page.logged_in import HomePageLoggedIn
from umspages.portal.home_page.logged_out import HomePageLoggedOut


@pytest.fixture
def stub_announcement(udm_ldap_base):
    data = {
        "properties": {
            "allowedGroups": [],
            "isSticky": False,
            "message": {
                "en_US": "Message content of E2E Test Announcement e2e-test-001."
            },
            "name": "e2e-test-001",
            "needsConfirmation": False,
            "objectFlag": [],
            "severity": "warn",
            "title": {"en_US": "E2E Test Announcement Title"},
            "visibleFrom": None,
            "visibleUntil": None,
        },
        "position": f"cn=announcement,cn=portals,cn=univention,{udm_ldap_base}",
    }
    return data


def test_anonymous_user_sees_announcement(
    udm_fixtures, navigate_to_home_page_logged_out, stub_announcement
):
    announcement_data = udm_fixtures.ensure_announcement(stub_announcement)
    page = navigate_to_home_page_logged_out
    home_page = HomePageLoggedOut(page)
    expected_title = announcement_data["properties"]["title"]["en_US"]
    home_page.announcement_container.assert_announcement(title=expected_title)


def test_admin_user_can_view_announcements_page(
    navigate_to_home_page_logged_in_as_admin,
):
    page = navigate_to_home_page_logged_in_as_admin
    home_page_logged_in = HomePageLoggedIn(page)
    announcements_page = AnnouncementsPage(
        home_page_logged_in.click_announcements_tile()
    )
    expect(announcements_page.add_button).to_be_visible()
