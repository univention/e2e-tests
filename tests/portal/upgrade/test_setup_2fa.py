# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH
import json
from dataclasses import dataclass
from typing import Any

import pytest
from playwright.sync_api import BrowserContext, Page

from umspages.portal.login_page import LoginPage, TotpSetup


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
def existing_twofa_user(udm, ldap_base_dn: str, upgrade_artifacts_path):
    """
    Loads a user from the upgrade_artifacts_path.
    Yields a dict with "username", "password" and "totp_secret".

    This user is deleted during the cleanup of this fixture.
    """
    assert upgrade_artifacts_path
    with open(upgrade_artifacts_path, "r") as fd:
        backup = json.load(fd)

    yield backup

    users_user = udm.get("users/user")
    user_dn = f"uid={backup['username']},cn=users,{ldap_base_dn}"
    test_user = users_user.get(user_dn)

    test_user.delete()


@pytest.mark.pre_upgrade
def test_setup_2fa_user(context: BrowserContext, twofa_user, user_password, upgrade_artifacts_path):
    assert upgrade_artifacts_path

    username = twofa_user.properties["username"]

    totp_setup = TotpSetup(secret=None)
    page = context.new_page()
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(twofa_user.properties["username"], user_password, totp_setup=totp_setup)
    page.close()

    assert totp_setup.secret, "TOTP secret not available after setup"

    backup = {
        "username": twofa_user.properties["username"],
        "password": user_password,
        "totp_secret": totp_setup.secret,
    }

    with open(upgrade_artifacts_path, "w") as fd:
        json.dump(backup, fd)

    # verify TOTP setup
    context.clear_cookies()
    page = context.new_page()
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(username, user_password, totp_secret=totp_setup.secret)


@pytest.mark.post_upgrade
def test_login_2fa(page: Page, existing_twofa_user: dict[str, Any]):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(
        existing_twofa_user["username"], existing_twofa_user["password"], totp_secret=existing_twofa_user["totp_secret"]
    )
