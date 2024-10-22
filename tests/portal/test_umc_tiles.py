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

# tests/portal/test_umc_tiles.py

import pytest

from umspages.common.base import expect
from umspages.portal.home_page.logged_in import HomePageLoggedIn
from umspages.portal.login_page import LoginPage
from umspages.portal.umc_section import UMCSection


@pytest.mark.login
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_umc_tiles(navigate_to_login_page, admin_username, admin_password, subtests):
    """Tests that all the expected and only the expected UMC tiles are present."""
    page = navigate_to_login_page
    login_page = LoginPage(page)
    login_page.login(admin_username, admin_password)
    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_in.assert_logged_in()

    umc_section = UMCSection(page.locator("h2:has-text('Univention Management Console')").locator(".."))
    expect(umc_section.section_title).to_be_visible()

    expected_structure = {
        "Users": ["Contacts", "Groups", "Users"],
        "Devices": ["Computers", "Printers"],
        "Domain": [
            "Blocklists",
            "DHCP",
            "DNS",
            "LDAP directory",
            "Mail",
            "Networks",
            "Policies",
            "Shares",
            # "OX Functional Accounts",
            # "OX Resources",
            "Portal",
            # "Portal Announcements",
        ],
    }

    with subtests.test(msg="Folder count"):
        umc_section.assert_folder_count(len(expected_structure))

    for folder_name, expected_items in expected_structure.items():
        with subtests.test(msg=f"Folder contents: {folder_name}"):
            umc_section.assert_folder_contents(folder_name, expected_items)

    with subtests.test(msg="All folders present"):
        umc_section.assert_all_folders_present(expected_structure.keys())

    all_expected_items = set(sum(expected_structure.values(), []))
    with subtests.test(msg="All items present"):
        umc_section.assert_all_items_present(all_expected_items)


@pytest.mark.login
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_regular_user_does_not_see_umc_section(navigate_to_login_page, user, user_password, wait_for_portal_sync):
    username = user.properties["username"]
    page = navigate_to_login_page
    wait_for_portal_sync(user, 2)

    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(username, user_password)

    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_in.assert_logged_in()

    umc_section = UMCSection(page.locator("body"))
    expect(umc_section.section_title).not_to_be_visible()
