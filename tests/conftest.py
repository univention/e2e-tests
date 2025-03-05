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

import logging
from urllib.parse import urljoin

import pytest
import requests

from api.maildev import MaildevApi
from univention.admin.rest.client import UDM, NotFound

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def admin_username(pytestconfig):
    return pytestconfig.option.admin_username


@pytest.fixture(scope="session")
def admin_password(pytestconfig):
    return pytestconfig.option.admin_password


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
    The URL to reach the Maildev API.

    This fixture does automatically flag test cases to be skipped if the URL is
    not configured. This way the test suite can reasonably be used to test
    deployments which don't have the full e2e testing support infrastructure
    available.
    """
    base_url = pytestconfig.option.email_test_api_base_url
    if not base_url:
        pytest.skip("Skipping, no email_test_api configuration provided.")
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
def udm(udm_factory, ldap):
    """
    A configured instance of the UDM Rest API client.

    This instance uses the most privileged user to access the directory. If you
    want a client for a particular user, then use the fixture `udm_factory`
    instead.
    """
    udm = udm_factory(ldap.admin_rdn, ldap.admin_password)
    return udm


@pytest.fixture(scope="session")
def udm_factory(udm_rest_api):
    """
    Returns a factory function to create a new UDM connection.

    Example::

       udm_factory("your-username", "your-password")

    """

    def factory(username, password) -> UDM:
        udm = UDM(udm_rest_api.base_url, username, password)
        _verify_udm_rest_api_configuration(udm)
        return udm

    return factory


def _verify_udm_rest_api_configuration(udm):
    ldap_base = udm.get_ldap_base()
    assert ldap_base


@pytest.fixture(scope="session")
def ldap_base_dn(udm) -> str:
    """
    Base DN of the LDAP directory.
    """
    return udm.get_ldap_base()


@pytest.fixture(scope="session")
def email_domain(udm):
    """
    Returns a valid email domain.

    The email domain is valid in the context of the system under test and
    discovered out of the configuration automatically.
    """
    mail_domains_module = udm.get("mail/domain")
    mail_domain = next(mail_domains_module.search()).open()
    return mail_domain.properties["name"]


@pytest.fixture
def external_email_domain(faker):
    """
    Returns an external email domain.

    External means that this domain is not managed by the system under test. It
    is intended for cases when a password recovery email shall be configured.
    """
    domain = f"{faker.domain_word()}.test"
    return domain


@pytest.fixture
def portal_udm(udm, faker, ldap_base_dn):
    """
    Creates a Portal object via UDM Rest API.

    The object is as minimal as possible and will be cleaned up after the test
    run.
    """
    portal_module = udm.get("portals/portal")
    portal_obj = portal_module.new()
    portal_name = f"test-{faker.slug()}"
    portal_obj.properties.update(
        {
            "name": portal_name,
            "displayName": {
                "en_US": faker.catch_phrase(),
            },
        }
    )
    portal_obj.save()

    yield portal_obj

    try:
        portal_obj.reload()
        portal_obj.delete()
    except NotFound:
        logger.info("Portal %s has been removed by the test case.", portal_obj.dn)


@pytest.fixture
def portal_entry(udm, faker, ldap_base_dn):
    """
    Creates an activated test Portal Entry.

    The Portal Entry will be isolated, it will not be added into any Portal or
    Category.

    The entry will be cleaned up after the test run.
    """
    entry_module = udm.get("portals/entry")
    portal_entry = entry_module.new()
    portal_entry.properties.update(
        {
            "name": f"test-{faker.slug()}",
            "description": {"en_US": faker.catch_phrase()},
            "displayName": {"en_US": faker.catch_phrase()},
            "link": [["en_US", "http://test.example.com"]],
            "activated": True,
        }
    )
    portal_entry.save()

    yield portal_entry

    try:
        portal_entry.reload()
        portal_entry.delete()
    except NotFound:
        logger.info("Portal Entry %s has been removed by the test case.", portal_entry.dn)
