# Like what you see? Join us!
# https://www.univention.com/about-us/careers/vacancies/
#
# Copyright 2001-2025 Univention GmbH
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
from playwright.sync_api import Page

from umspages.portal.home_page.logged_in import HomePageLoggedIn
from umspages.portal.login_page import LoginPage


@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_no_missing_icons(navigate_to_login_page: Page, admin_username, admin_password):
    """Tests that all the expected and only the expected UMC tiles are present."""
    page = navigate_to_login_page
    login_page = LoginPage(page)
    login_page.login(admin_username, admin_password)

    page = HomePageLoggedIn(page).page

    page.wait_for_selector("img", timeout=10000)
    img_elements = page.query_selector_all("img")

    found_users_svg = False
    for img in img_elements:
        src = img.get_attribute("src")
        if "users.svg" in src:
            found_users_svg = True
        assert src and "questionmark.svg" not in src, f"Found question mark image: {src}"

    assert found_users_svg, "Image users.svg not found in the page. Maybe portal is not loaded correctly."
