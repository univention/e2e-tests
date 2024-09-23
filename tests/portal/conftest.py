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
from datetime import datetime, timedelta
from typing import Callable
from urllib.parse import urljoin, urlparse

import pytest
import requests
from tenacity import before_sleep_log, retry, stop_after_delay, wait_fixed

from api.udm_api import UDMFixtures
from e2e.decorators import BetterRetryError
from umspages.portal.home_page.logged_in import HomePageLoggedIn
from umspages.portal.home_page.logged_out import HomePageLoggedOut
from umspages.portal.login_page import LoginPage

logger = logging.getLogger(__name__)


WaitForPortalSync = Callable[[str, int], None]


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, portal_base_url, keycloak_base_url):
    in_a_week = datetime.now() + timedelta(weeks=1)
    portal_cookie_domain = urlparse(portal_base_url).hostname
    keycloak_cookie_domain = urlparse(keycloak_base_url).hostname
    return {
        **browser_context_args,
        "base_url": portal_base_url,
        "locale": "en-US",
        "timezone_id": "Europe/Berlin",
        "storage_state": {
            # This is a slight violation of good end-to-end testing practices.
            # Nearly all of our tests want to check the system with the cookie
            # consent already given. This violation does make each of those
            # tests simpler.
            #
            # Tests which explicitly need fresh cookies can use e.g.
            # `pytest.mark.browser_context_args` or define this fixture in a
            # smaller scope to adjust things.
            "cookies": [
                {
                    "domain": f".{keycloak_cookie_domain}",
                    "expires": in_a_week.timestamp(),
                    "httpOnly": False,
                    "name": "univentionCookieSettingsAccepted",
                    "path": "/",
                    "sameSite": "Strict",
                    "secure": False,
                    "value": "do-not-change-me",
                },
                {
                    "domain": f".{portal_cookie_domain}",
                    "expires": in_a_week.timestamp(),
                    "httpOnly": False,
                    "name": "univentionCookieSettingsAccepted",
                    "path": "/",
                    "sameSite": "Strict",
                    "secure": False,
                    "value": "do-not-change-me",
                },
            ],
            "origins": [],
        },
    }


@pytest.fixture()
def navigate_to_home_page_logged_out(page):
    home_page_logged_out = HomePageLoggedOut(page)
    home_page_logged_out.navigate()
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
def navigate_to_home_page_logged_in(page, admin_username, admin_password):
    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_in.navigate(admin_username, admin_password)
    return page


@pytest.fixture()
def navigate_to_home_page_logged_in_as_admin(page, admin_username, admin_password):
    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_in.navigate(admin_username, admin_password)
    return page


@pytest.fixture(scope="session")
def udm_session(admin_username, admin_password):
    """
    Prepares an instance of `requests.Session` to call the UDM Rest API.

    The instance has headers and authentication information prepared so that
    requests will run with full permissions in the UDM Rest API.
    """
    udm_session = requests.Session()
    udm_session.auth = (admin_username, admin_password)
    udm_session.headers.update({"accept": "application/json"})
    return udm_session


@pytest.fixture()
def udm_fixtures(udm_rest_api_base_url, udm_session):
    """An instance of `UDMFixtures` to set up test data through the UDM Rest API."""
    return UDMFixtures(base_url=udm_rest_api_base_url, session=udm_session)


@pytest.fixture
def block_expiration_duration(pytestconfig):
    return pytestconfig.option.release_duration


@pytest.fixture
def failed_attempts_before_ip_block(pytestconfig):
    return pytestconfig.option.num_ip_block


@pytest.fixture
def navigation_api_url(portal_base_url):
    """URL of the navigation API in the Portal."""
    return urljoin(portal_base_url, "/univention/portal/navigation.json")


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
def user_password(faker):
    """
    The password used for the fixture ``user``.

    This is split out so that it can be accessed easily. The UDM object
    ``user`` does not contain the password itself anymore.
    """
    return faker.password()


@pytest.fixture
def user(udm, faker, email_domain, external_email_domain, user_password, wait_for_ldap_secondaries_to_catch_up):
    """
    A regular user.

    The user will be created for the test case and removed after the test case.

    The password is available in the fixture ``user_password``.
    """
    users_user = udm.get("users/user")
    test_user = users_user.new()
    username = f"test-{faker.user_name()}"

    test_user.properties.update(
        {
            "firstname": faker.first_name(),
            "lastname": faker.last_name(),
            "username": username,
            "displayName": faker.name(),
            "password": user_password,
            "mailPrimaryAddress": f"{username}@{email_domain}",
            "PasswordRecoveryEmail": f"{username}@{external_email_domain}",
        }
    )
    test_user.save()

    wait_for_ldap_secondaries_to_catch_up()
    yield test_user

    test_user.reload()
    test_user.delete()


def has_central_navigation_categories(response: requests.Response, minimum_categories):
    return len(response.json()["categories"]) >= minimum_categories


@pytest.fixture
def wait_for_portal_sync(navigation_api_url, portal_central_navigation_secret) -> WaitForPortalSync:
    """
    Allows to wait until the portal data for a user is complete.
    """

    def _wait_for_portal_json(username: str, minimum_categories: int, timeout: int | float = 120) -> None:
        @retry(
            stop=stop_after_delay(timeout),
            wait=wait_fixed(0.25),
            before_sleep=before_sleep_log(logger, logging.INFO),
            retry_error_cls=BetterRetryError,
        )
        def poll_central_navigation():
            result = requests.get(navigation_api_url, auth=(username, portal_central_navigation_secret))
            if not has_central_navigation_categories(result, minimum_categories):
                raise Exception(f"Portal tiles for user {username} are not (yet) up to date")

        poll_central_navigation()

    return _wait_for_portal_json


@pytest.fixture
def testing_api_base_url(portal_base_url):
    return f"{portal_base_url}/testing-api/v1"


@pytest.fixture
def wait_for_ldap_secondaries_to_catch_up(testing_api_base_url) -> Callable[[], None]:
    """
    Allows to wait until all ldap server secondaries have caught up
    to the primary at the point of calling this function
    """

    def _wait_for_ldap_replication(retry_timeout: float = 90) -> None:
        response = requests.get(
            f"{testing_api_base_url}/ldap-replication-waiter",
            {"retry_timeout": retry_timeout},
        )
        response.raise_for_status()

    return _wait_for_ldap_replication
