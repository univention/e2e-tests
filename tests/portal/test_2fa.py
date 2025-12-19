# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH
import json
from dataclasses import dataclass

import pytest
from playwright.sync_api import BrowserContext, Page

from umspages.portal.home_page.logged_in import HomePageLoggedIn
from umspages.portal.login_page import TotpSetup


@dataclass
class UpgradeBackup:
    username: str
    password: str
    totp_secret: str


@pytest.fixture
def twofa_user(
    udm, faker, email_domain, external_email_domain, user_password, wait_for_ldap_secondaries_to_catch_up, ldap_base_dn
):
    """
    A regular user in the 2FA Users group.

    The user will be created for the test case and is *not* removed after the test case
    so that it can be re-used in the post-upgrade tests.

    The password is available in the fixture ``user_password``.
    """
    users_user = udm.get("users/user")
    test_user = users_user.new()
    # Test 2FA setup specifically with a mixed case username
    # https://github.com/keycloak/keycloak/issues/43621
    uppercase_username_prefix = "TEST"
    username = f"{uppercase_username_prefix}-{faker.user_name()}"

    test_user.properties.update(
        {
            "firstname": faker.first_name(),
            "lastname": faker.last_name(),
            "username": username,
            "displayName": faker.name(),
            "password": user_password,
            "mailPrimaryAddress": f"{username}@{email_domain}",
            "PasswordRecoveryEmail": f"{username}@{external_email_domain}",
            "groups": [f"cn=2FA Users,cn=groups,{ldap_base_dn}"],
        }
    )
    test_user.save()

    wait_for_ldap_secondaries_to_catch_up()

    return test_user


@pytest.fixture
def temp_twofa_user(twofa_user):
    """
    Returns a UDM user object where the user is part of the
    "2FA Users" group and therefore forced to setup Totp.

    The user is automatically deleted after the test.
    """
    yield twofa_user

    twofa_user.reload()
    twofa_user.delete()


@pytest.fixture
def persistent_twofa_user(twofa_user, user_password, upgrade_artifacts_path):
    """
    Creates a user and yields a tuple with a dict containing the
    "username" and "password" of the user as the first element
    and an instance of TotpSetup as the second element to be passed to the
    login function.

    The user is part of the "2FA Users" group and therefore forced to setup TOTP.

    The user is not deleted after the test for use in an upgrade scenario.
    For an auto deleting 2FA user see the `temp_twofa_user` fixture.
    """
    totp_setup = TotpSetup(secret=None)

    backup = {
        "username": twofa_user.properties["username"],
        "password": user_password,
    }

    yield (backup, totp_setup)

    assert totp_setup.secret, "Secret is not set after totp login"

    backup["totp_secret"] = totp_setup.secret

    with open(upgrade_artifacts_path, "w") as fd:
        json.dump(backup, fd)


@pytest.fixture
def existing_twofa_user(udm, ldap_base_dn: str, upgrade_artifacts_path):
    """
    Loads a user from the upgrade_artifacts_path.
    Yields a tuple with a dict "username", "password" as the first element
    and an instance of "TotpSetup" to be passed to the login function.

    This user is deleted during the cleanup of this fixture.
    """
    assert upgrade_artifacts_path
    with open(upgrade_artifacts_path, "r") as fd:
        backup = json.load(fd)

    totp_setup = TotpSetup(secret=backup["totp_secret"])

    yield (backup, totp_setup)

    users_user = udm.get("users/user")
    user_dn = f"uid={backup['username']},cn=users,{ldap_base_dn}"
    test_user = users_user.get(user_dn)

    test_user.delete()


def setup_totp(page: Page, username: str, user_password: str, totp_setup: TotpSetup):
    login_page = HomePageLoggedIn(page)
    login_page.navigate(username, user_password, totp_setup)
    page.close()


def login_totp(page: Page, username: str, user_password: str, totp_setup: TotpSetup):
    login_page = HomePageLoggedIn(page)
    login_page.navigate(username, user_password, totp_setup)


def setup_and_login_totp(context: BrowserContext, username: str, user_password: str, totp_setup: TotpSetup):
    page = context.new_page()
    setup_totp(page, username, user_password, totp_setup)
    page.close()

    assert totp_setup.secret, "TOTP secret not available after setup"

    context.clear_cookies()
    page = context.new_page()
    login_totp(page, username, user_password, totp_setup)


@pytest.mark.pre_upgrade
def test_setup_2fa_user(context: BrowserContext, persistent_twofa_user):
    twofa_user, totp_setup = persistent_twofa_user
    setup_and_login_totp(context, twofa_user["username"], twofa_user["password"], totp_setup)


@pytest.mark.post_upgrade
def test_login_2fa_after_upgrade(page: Page, existing_twofa_user):
    twofa_user, totp_setup = existing_twofa_user
    login_totp(page, twofa_user["username"], twofa_user["password"], totp_setup)


@pytest.mark.portal
@pytest.mark.acceptance_environment
def test_login_2fa(context: BrowserContext, temp_twofa_user, user_password):
    totp_setup = TotpSetup(secret=None)

    setup_and_login_totp(context, temp_twofa_user.properties["username"], user_password, totp_setup)
