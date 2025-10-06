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
import requests

from umspages.portal.home_page.logged_in import HomePageLoggedIn
from umspages.portal.home_page.logged_out import HomePageLoggedOut
from umspages.portal.login_page import LoginPage


@pytest.mark.login
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_login(navigate_to_login_page, admin_username, admin_password):
    """Tests OIDC login by default"""
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
    """Tests OIDC logout by default"""
    page = navigate_to_login_page
    login_page = LoginPage(page)
    login_page.login(admin_username, admin_password)
    home_page_logged_in = HomePageLoggedIn(page)

    home_page_logged_in.reveal_area(home_page_logged_in.right_side_menu, home_page_logged_in.header.hamburger_icon)
    home_page_logged_in.right_side_menu.click_logout_button()

    home_page_logged_out = HomePageLoggedOut(page)
    home_page_logged_out.assert_logged_out()


@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.skip(reason="SAML endpoints are not exposed in Kubernetes deployments (disabled by default)")
def test_saml_login(navigate_to_saml_login_page, admin_username, admin_password):
    """Tests SAML login specifically to ensure it still works (only when SAML is enabled)"""
    page = navigate_to_saml_login_page
    login_page = LoginPage(page)
    login_page.login(admin_username, admin_password)

    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_in.assert_logged_in()


@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.skip(reason="SAML endpoints are not exposed in Kubernetes deployments (disabled by default)")
def test_saml_logout(navigate_to_saml_login_page, admin_username, admin_password):
    """Tests SAML logout specifically (only when SAML is enabled)"""
    page = navigate_to_saml_login_page
    login_page = LoginPage(page)
    login_page.login(admin_username, admin_password)
    home_page_logged_in = HomePageLoggedIn(page)

    home_page_logged_in.reveal_area(home_page_logged_in.right_side_menu, home_page_logged_in.header.hamburger_icon)
    home_page_logged_in.right_side_menu.click_logout_button()

    home_page_logged_out = HomePageLoggedOut(page)
    home_page_logged_out.assert_logged_out()


@pytest.mark.parametrize(
    "login_method,navigate_fixture",
    [
        ("oidc", "navigate_to_oidc_login_page"),
        pytest.param(
            "saml",
            "navigate_to_saml_login_page",
            marks=pytest.mark.skip(
                reason="SAML endpoints are not exposed in Kubernetes deployments (disabled by default)"
            ),
        ),
    ],
)
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_login_methods_and_tiles(request, login_method, navigate_fixture, admin_username, admin_password):
    """Test both OIDC and SAML login work and display tiles correctly"""
    page = request.getfixturevalue(navigate_fixture)
    login_page = LoginPage(page)
    login_page.login(admin_username, admin_password)

    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_in.assert_logged_in()

    # Verify that we can see tiles after login (basic smoke test)
    home_page_logged_in.is_displayed()


@pytest.mark.portal
@pytest.mark.acceptance_environment
def test_saml_endpoint_not_exposed(portal):
    """Verify SAML endpoints are not publicly accessible (disabled by default)"""
    response = requests.get(f"{portal.base_url}/univention/saml/", allow_redirects=False)

    assert response.status_code in [
        403,
        404,
    ], f"SAML endpoint should not be accessible, got status {response.status_code}"


@pytest.mark.portal
@pytest.mark.acceptance_environment
def test_only_oidc_login_tile_visible(navigate_to_home_page_logged_out):
    """Verify that only OIDC login tile is visible (SAML disabled by default)"""
    page = navigate_to_home_page_logged_out
    home_page = HomePageLoggedOut(page)

    assert home_page.has_oidc_login_tile(), "OIDC login tile should be visible"
    assert not home_page.has_saml_login_tile(), "SAML login tile should not be visible (disabled by default)"
