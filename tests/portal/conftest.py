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

from urllib.parse import urljoin

import pytest
import requests

from api.udm_api import UDMFixtures
from umspages.portal.home_page.logged_in import HomePageLoggedIn
from umspages.portal.home_page.logged_out import HomePageLoggedOut
from umspages.portal.login_page import LoginPage
from umspages.portal.selfservice.logged_in import SelfservicePortalLoggedIn
from umspages.portal.selfservice.logged_out import SelfservicePortalLoggedOut


@pytest.fixture(scope="session")
def username(pytestconfig):
    return pytestconfig.option.username


@pytest.fixture(scope="session")
def password(pytestconfig):
    return pytestconfig.option.password


@pytest.fixture(scope="session")
def admin_username(pytestconfig):
    return pytestconfig.option.admin_username


@pytest.fixture(scope="session")
def admin_password(pytestconfig):
    return pytestconfig.option.admin_password


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, portal_base_url):
    browser_context_args["base_url"] = portal_base_url
    return browser_context_args


@pytest.fixture()
def navigate_to_home_page_logged_out(page):
    home_page_logged_out = HomePageLoggedOut(page)
    home_page_logged_out.navigate()
    return page


@pytest.fixture()
def navigate_to_selfservice_portal_logged_out(page):
    selfservice_portal_logged_out = SelfservicePortalLoggedOut(page)
    selfservice_portal_logged_out.navigate()
    return page


@pytest.fixture()
def navigate_to_login_page(page):
    login_page = LoginPage(page)
    login_page.navigate()
    return page


@pytest.fixture()
def navigate_to_saml_login_page(page):
    login_page = LoginPage(page)
    login_page.navigate_saml()
    return page


@pytest.fixture()
def navigate_to_home_page_logged_in(page, username, password):
    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_in.navigate(username, password)
    return page


@pytest.fixture()
def navigate_to_selfservice_portal_logged_in(page, username, password):
    selfservice_portal_logged_in = SelfservicePortalLoggedIn(page)
    selfservice_portal_logged_in.navigate(username, password)
    return page


@pytest.fixture()
def navigate_to_home_page_logged_in_as_admin(page, admin_username, admin_password):
    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_in.navigate(admin_username, admin_password)
    return page


@pytest.fixture(scope="session")
def udm_session(udm_admin_username, udm_admin_password):
    """
    Prepares an instance of `requests.Session` to call the UDM Rest API.

    The instance has headers and authentication information prepared so that
    requests will run with full permissions in the UDM Rest API.
    """
    udm_session = requests.Session()
    udm_session.auth = (udm_admin_username, udm_admin_password)
    udm_session.headers.update({"accept": "application/json"})
    return udm_session


@pytest.fixture()
def udm_fixtures(udm_rest_api_base_url, udm_session):
    """An instance of `UDMFixtures` to set up test data through the UDM Rest API."""
    return UDMFixtures(base_url=udm_rest_api_base_url, session=udm_session)


@pytest.fixture()
def udm_ldap_base(udm_rest_api_base_url, udm_session):
    """
    The base DN used by the LDAP directory behind the UDM Rest API.

    This value is dynamically discovered and will only be available if the UDM
    Rest API is up and running.
    """
    ldap_base_url = urljoin(udm_rest_api_base_url, "ldap/base/")
    result = udm_session.get(ldap_base_url)
    data = result.json()
    return data["dn"]


@pytest.fixture
def block_expiration_duration(pytestconfig):
    return pytestconfig.option.release_duration


@pytest.fixture
def failed_attempts_before_ip_block(pytestconfig):
    return pytestconfig.option.num_ip_block
