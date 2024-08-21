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
from univention.admin.rest.client import UDM

from api.maildev import MaildevApi


def pytest_addoption(parser):
    # Portal tests options
    parser.addoption("--portal-base-url", help="Base URL of the univention portal")
    parser.addoption("--username", help="Portal login username")
    parser.addoption("--password", help="Portal login password")
    parser.addoption("--admin-username", help="Portal admin login username")
    parser.addoption("--admin-password", help="Portal admin login password")
    parser.addoption(
        "--udm-admin-username", default="cn=admin", help="UDM admin login password"
    )
    parser.addoption(
        "--udm-admin-password", default="univention", help="UDM admin login password"
    )
    parser.addoption(
        "--email-test-api-username", default="user", help="Username to access the email test API.")
    parser.addoption(
        "--email-test-api-password",
        default="univention",
        help="Password to access the email test API."
    )
    parser.addoption(
        "--email-test-api-base-url",
        default="",
        help="Base URL to reach the email test API (Maildev).",
    )
    parser.addoption(
        "--portal-central-navigation-secret",
        default="univention",
        help="Shared secret with portal-server for central navigation",
    )
    # BFP tests options
    parser.addoption("--keycloak-base-url", help="Base URL of Keycloak")
    parser.addoption(
        "--kc-admin-username", default="admin", help="Keycloak admin login username"
    )
    parser.addoption(
        "--kc-admin-password",
        default="univention",
        help="Keycloak admin login password",
    )
    parser.addoption(
        "--num-device-block",
        type=int,
        default=5,
        help="Number of failed logins for device block",
    )
    parser.addoption(
        "--num-ip-block",
        type=int,
        default=7,
        help="Number of failed logins for IP block",
    )
    parser.addoption(
        "--release-duration",
        type=int,
        default=1,
        help="Blocks are released after this many minutes",
    )
    parser.addoption("--realm", default="master", help="Realm to attempt logins at")


@pytest.fixture(scope="session")
def udm_admin_username(pytestconfig):
    return pytestconfig.option.udm_admin_username


@pytest.fixture(scope="session")
def udm_admin_password(pytestconfig):
    return pytestconfig.option.udm_admin_password


@pytest.fixture(scope="session")
def portal_base_url(pytestconfig):
    return pytestconfig.getoption("--portal-base-url")


@pytest.fixture(scope="session")
def keycloak_base_url(pytestconfig):
    return pytestconfig.getoption("--keycloak-base-url")


@pytest.fixture(scope="session")
def email_test_api_username(pytestconfig):
    """
    The username required to access the email test API.
    """
    return pytestconfig.option.email_test_api_username


@pytest.fixture(scope="session")
def email_test_api_password(pytestconfig):
    """
    The password required to access the email test API.
    """
    return pytestconfig.option.email_test_api_password

@pytest.fixture(scope="session")
def email_test_api_base_url(pytestconfig):
    """
    The password required to access the email test API.
    """
    base_url = pytestconfig.option.email_test_api_base_url
    if not base_url:
        raise pytest.UsageError("E-Mail test API base URL is not provided.")
    return base_url

@pytest.fixture(scope="session")
def email_test_api_session(email_test_api_username, email_test_api_password, email_test_api_base_url):
    """
    Prepares an instance of `requests.Session` to call the Maildev API

    The object is configured with the user credentials, so that the users don't
    have to deal with the authentication details of the api.
    """
    api_session = requests.Session()
    api_session.auth = (email_test_api_username, email_test_api_password)
    api_session.headers.update({"accept": "application/json"})
    _verify_email_test_api_configuration(api_session, base_url=email_test_api_base_url)
    return api_session


def _verify_email_test_api_configuration(api_session, base_url):
    # Using the config endpoint since the health endpoint does not require
    # authentication.
    config_url = urljoin(base_url, "/config")
    response = api_session.get(config_url)
    response.raise_for_status()


@pytest.fixture(scope="session")
def email_test_api(email_test_api_session, email_test_api_base_url):
    """
    An instance of `api.maildev.MaildevApi` preconfigured.
    """
    return MaildevApi(email_test_api_base_url, email_test_api_session)


@pytest.fixture(scope="session")
def portal_central_navigation_secret(pytestconfig):
    return pytestconfig.getoption("--portal-central-navigation-secret")


@pytest.fixture(scope="session")
def udm_rest_api_base_url(portal_base_url):
    """Base URL to reach the UDM Rest API."""
    return urljoin(portal_base_url, "/univention/udm/")


@pytest.fixture(scope="session")
def udm(udm_rest_api_base_url, udm_admin_username, udm_admin_password):
    """
    A configured instance of the UDM Rest API client.
    """
    udm = UDM(udm_rest_api_base_url, udm_admin_username, udm_admin_password)
    _verify_udm_rest_api_configuration(udm)
    return udm


def _verify_udm_rest_api_configuration(udm):
    ldap_base = udm.get_ldap_base()
    assert ldap_base
