# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import pytest
from playwright.sync_api import Page

from e2e.password_hashes import assert_password_hashes, read_password_hashes
from umspages.portal.home_page.logged_in import HomePageLoggedIn
from umspages.portal.users.users_page import UCSUsersPage


@pytest.mark.selfservice
@pytest.mark.portal
@pytest.mark.password_hashes
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_create_user_via_the_umc(
    navigate_to_home_page_logged_in_as_admin: Page,
    faker,
    udm,
    ldap_primary,
    subtests,
):
    username = faker.user_name()
    password = faker.password()
    page = navigate_to_home_page_logged_in_as_admin
    home_page_logged_in = HomePageLoggedIn(page)

    home_page_logged_in.click_users_tile()
    users_page = home_page_logged_in
    users_page = UCSUsersPage(home_page_logged_in.page)
    users_page.add_user_button.click()
    users_page.add_user_dialog.add_user(username=username, password=password)

    users_user = udm.get("users/user")
    user = next(users_user.search(f"uid={username}")).open()

    assert user
    assert user.properties["univentionObjectIdentifier"]

    with subtests.test("password hashes"):
        entry = read_password_hashes(ldap_primary, user.dn)
        assert_password_hashes(entry, user.dn, key_version_number=1)

    user.delete()
