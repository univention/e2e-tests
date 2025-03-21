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

from e2e.decorators import retrying_slow
from umspages.common.base import expect
from umspages.portal.home_page.base import HomePage


@pytest.fixture
def stub_announcement_data(faker, ldap_base_dn):
    data = {
        "properties": {
            "allowedGroups": [],
            "isSticky": False,
            "message": {"en_US": "Message content of E2E Test Announcement e2e-test-001."},
            "name": faker.numerify("e2e-test-%###"),
            "needsConfirmation": False,
            "objectFlag": [],
            "severity": "warn",
            "title": {"en_US": "E2E Test Announcement Title"},
            "visibleFrom": None,
            "visibleUntil": None,
        },
        "position": f"cn=announcement,cn=portals,cn=univention,{ldap_base_dn}",
    }
    return data


@pytest.fixture
def stub_announcement(stub_announcement_data, udm_fixtures):
    announcement = udm_fixtures.ensure_announcement(stub_announcement_data)
    yield announcement
    udm_fixtures.delete_resource(announcement)


@pytest.mark.announcements
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_anonymous_user_sees_announcement(page, stub_announcement):
    home_page = HomePage(page)

    @retrying_slow
    def assert_announcement_is_visible():
        home_page.navigate()
        expected_title = stub_announcement["properties"]["title"]["en_US"]
        title = home_page.announcement_container.get_title(title=expected_title)
        expect(title).to_be_visible(timeout=1000)

    assert_announcement_is_visible()
