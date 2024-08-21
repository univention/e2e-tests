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

from umspages.portal.home_page.logged_in import HomePageLoggedIn
from umspages.portal.home_page.logged_out import HomePageLoggedOut
from umspages.portal.login_page import LoginPage


@pytest.mark.login
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_login(navigate_to_login_page, admin_username, admin_password):
    """Tests the plain UMC login in our devenv but the SAML login in the nightly deployment"""
    page = navigate_to_login_page
    login_page = LoginPage(page)
    login_page.login(admin_username, admin_password)

    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_in.assert_logged_in()


@pytest.mark.logout
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_logout(navigate_to_login_page, admin_username, admin_password):
    """Tests the plain UMC logout in our devenv but the SAML login in the nightly deployment"""
    page = navigate_to_login_page
    login_page = LoginPage(page)
    login_page.login(admin_username, admin_password)
    home_page_logged_in = HomePageLoggedIn(page)

    home_page_logged_in.reveal_area(home_page_logged_in.right_side_menu, home_page_logged_in.header.hamburger_icon)
    home_page_logged_in.right_side_menu.click_logout_button()

    home_page_logged_out = HomePageLoggedOut(page)
    home_page_logged_out.assert_logged_out()


@pytest.mark.saml()
def test_saml_login(navigate_to_saml_login_page, admin_username, admin_password):
    page = navigate_to_saml_login_page
    login_page = LoginPage(page)
    login_page.login(admin_username, admin_password)

    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_in.assert_logged_in()


@pytest.mark.saml()
def test_saml_logout(navigate_to_saml_login_page, admin_username, admin_password):
    page = navigate_to_saml_login_page
    login_page = LoginPage(page)
    login_page.login(admin_username, admin_password)
    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_in.assert_logged_in()

    home_page_logged_in.reveal_area(home_page_logged_in.right_side_menu, home_page_logged_in.header.hamburger_icon)
    home_page_logged_in.right_side_menu.click_logout_button()

    home_page_logged_out = HomePageLoggedOut(page)
    home_page_logged_out.assert_logged_out()
