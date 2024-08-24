# Like what you see? Join us!
# https://www.univention.com/about-us/careers/vacancies/
#
# Copyright 2001-2024 Univention GmbH
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

from umspages.keycloak.on_block_page import OnIPBlockPage
from umspages.portal.home_page.logged_in import HomePageLoggedIn
from umspages.portal.login_page import LoginPage


@pytest.mark.acceptance_environment
def test_portal_login_ip_block(
    navigate_to_login_page,
    username,
    password,
    failed_attempts_before_ip_block,
    block_expiration_duration,
    pytestconfig,
):
    """
    Tests the brute-force protection component IP block is working.

    1. Attempt a given number of logins with wrong credentials.
    2. Expects the IP block message to appear.
    3. Waits for the IP block to expire.
    4. Attempts to login with valid credentials.

    > Limitations: it only tests from one IP, not ensuring login can happen
      from another IP. That is tested on the standalone version of this test.
    """

    if not pytestconfig.getoption("headed"):
        pytest.skip(reason="WIP: This test only works in headed mode.")

    page = navigate_to_login_page
    login_page = LoginPage(page)
    for _ in range(failed_attempts_before_ip_block):
        login_page.login(username, f"{password}_wrong_password")
        expect(login_page.page.get_by_text("Invalid username or password.")).to_be_visible(timeout=4000)
    # keycloak-extensions handler processes all the failed login events every
    # two seconds
    page.wait_for_timeout(2200)
    login_page.login(username, f"{password}_wrong_password")
    ip_block_page = OnIPBlockPage(page)
    ip_block_page.is_displayed()

    # + 1 for safety
    page.wait_for_timeout(round(block_expiration_duration * 60 * 1000) + 1)
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(username, password)
    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_in.assert_logged_in()
