# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

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
import re
from datetime import datetime, timedelta
from urllib.parse import urlparse

import pytest

from umspages.common.base import expect
from umspages.keycloak.login_page import LoginPage


@pytest.fixture
def locked_user(
    udm,
    faker,
    email_domain,
    external_email_domain,
    locked_user_password,
    wait_for_ldap_secondaries_to_catch_up,
):
    """
    A locked user.

    The user will be created for the test case and removed after the test case.

    The password is available in the fixture ``locked_user_password``.
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
            "password": f"!{locked_user_password}",
            "mailPrimaryAddress": f"{username}@{email_domain}",
            "PasswordRecoveryEmail": f"{username}@{external_email_domain}",
            "locked": True,
        }
    )
    test_user.save()

    wait_for_ldap_secondaries_to_catch_up()
    yield test_user

    test_user.reload()
    test_user.delete()


@pytest.fixture
def locked_user_password(faker):
    """
    The password used for the fixture ``locked_user``.

    This is split out so that it can be accessed easily. The UDM object
    ``locked_user`` does not contain the password itself anymore.
    """
    return faker.password()


@pytest.fixture
def expired_user(
    udm,
    faker,
    email_domain,
    external_email_domain,
    expired_user_password,
    wait_for_ldap_secondaries_to_catch_up,
):
    """
    An expired user.

    The user will be created for the test case and removed after the test case.

    The password is available in the fixture ``expired_user_password``.
    """
    users_user = udm.get("users/user")
    test_user = users_user.new()
    username = f"test-{faker.user_name()}"

    expiry_date = datetime.now() - timedelta(10)

    test_user.properties.update(
        {
            "firstname": faker.first_name(),
            "lastname": faker.last_name(),
            "username": username,
            "displayName": faker.name(),
            "password": expired_user_password,
            "mailPrimaryAddress": f"{username}@{email_domain}",
            "PasswordRecoveryEmail": f"{username}@{external_email_domain}",
            "userexpiry": expiry_date.strftime("%Y-%m-%d"),
        }
    )
    test_user.save()

    wait_for_ldap_secondaries_to_catch_up()
    yield test_user

    test_user.reload()
    test_user.delete()


@pytest.fixture
def expired_user_password(faker):
    """
    The password used for the fixture ``expired_user``.

    This is split out so that it can be accessed easily. The UDM object
    ``expired_user`` does not contain the password itself anymore.
    """
    return faker.password()


@pytest.mark.login
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
@pytest.mark.parametrize("language_code, language_name", [("en", "English"), ("de", "Deutsch")])
@pytest.mark.skip
def test_keycloak_user_locked_message(
    navigate_to_login_page,
    locked_user,
    locked_user_password,
    language_code,
    language_name,
):
    """
    Test the error message translation for a locked account in Keycloak.

    Test is skipped, because of unclear locking mechanism im UDM.
    A user account is disabled in UDM with:
        - krb5KDCFlags is changed
        - userPassword gets the ! in front of it
        - shadowExpire is set differently (I guess to 1)
        - sambaAcctFlags contains a D for "disabled"
    """
    expected_messages = {
        "en": "The account is locked.",
        "de": "Das Benutzerkonto ist abgelaufen.",
    }

    # Go to login page
    page = navigate_to_login_page
    login_page = LoginPage(page)

    # Set language
    if not login_page.current_language == language_code:
        login_page.switch_language(language_name)

    # Try a login
    login_page.login(locked_user.properties["username"], locked_user_password)

    expect(
        login_page.page.locator("#kc-form div").filter(has_text=expected_messages[language_code]).first
    ).to_be_visible()


@pytest.mark.login
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
@pytest.mark.parametrize("language_code, language_name", [("en", "English"), ("de", "Deutsch")])
def test_keycloak_user_expired_messages(
    navigate_to_login_page,
    expired_user,
    expired_user_password,
    language_code,
    language_name,
):
    """
    Test the error code translation in keycloak for an expired user account.
    """
    expected_messages = {
        "en": "The account has expired.",
        "de": "Das Benutzerkonto ist abgelaufen.",
    }
    # Go to login page
    page = navigate_to_login_page
    login_page = LoginPage(page)

    # Set language
    if not login_page.current_language == language_code:
        login_page.switch_language(language_name)

    # Try a login
    login_page.login(expired_user.properties["username"], expired_user_password)

    expect(
        login_page.page.locator("#kc-form div").filter(has_text=expected_messages[language_code]).first
    ).to_be_visible()


@pytest.mark.login
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
@pytest.mark.parametrize("language_code, language_name", [("en", "English"), ("de", "Deutsch")])
def test_keycloak_login_page_title_html(
    navigate_to_login_page,
    language_code,
    language_name,
    portal,
):
    """
    Test the login title translation in keycloak for an expired user account.
    """
    # Extract main domain from portal domain
    #   e.g. portal.example.com => example.com
    portal_domain = urlparse(portal.base_url).hostname
    domain = re.findall(r"(^.*\.|^)portal\.(.*)$", portal_domain)[0][1]

    expected_titles = {
        "en": f"Login at {domain}",
        "de": f"Anmelden bei {domain}",
    }

    # Go to login page
    page = navigate_to_login_page
    login_page = LoginPage(page)

    # Set language
    if not login_page.current_language == language_code:
        login_page.switch_language(language_name)

    expect(login_page.page.get_by_text(expected_titles[language_code]).first).to_be_visible()
