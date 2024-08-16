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

import random
import time
from typing import Tuple

import pytest
from playwright.sync_api import Page

from e2e.email.password_reset import PasswordResetEmail
from umspages.common.base import expect
from umspages.portal.home_page.logged_in import HomePageLoggedIn
from umspages.portal.home_page.logged_out import HomePageLoggedOut
from umspages.portal.selfservice.change_password import \
    ChangePasswordDialogPage
from umspages.portal.selfservice.logged_in import SelfservicePortalLoggedIn
from umspages.portal.selfservice.logged_out import SelfservicePortalLoggedOut
from umspages.portal.selfservice.manage_profile import ManageProfileDialogPage
from umspages.portal.selfservice.set_new_password import SetNewPasswordPage
from umspages.portal.selfservice.set_recovery_email import \
    SetRecoveryEmailDialogPage
from umspages.portal.users.users_page import UsersPage

DUMMY_USER_PASSWORD_1 = "firstpass"
DUMMY_USER_PASSWORD_2 = "secondpass"
DUMMY_EMAIL = "mail@example.org"
DUMMY_DESCRIPTION = "some description"


@pytest.fixture()
def dummy_username():
    yield f"dummy_{random.randint(1000, 9999)}"  # noqa: S311


@pytest.fixture()
def dummy_user_home(
    navigate_to_home_page_logged_in_as_admin: Page,
    admin_username,
    admin_password,
    dummy_username,
) -> Page:
    """
    Creates a dummy user from the UI.

    1. Logs in as an admin user.
    2. Creates a dummy user from the `Users` tile.
    3. Logs out from admin.
    4. Yields the page and the created username.
    5. Logs in as an admin user.
    6. Deletes the dummy user from step 2.
    """
    page = navigate_to_home_page_logged_in_as_admin
    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_out = HomePageLoggedOut(page)

    users_page = UsersPage(home_page_logged_in.click_users_tile())
    users_page.add_user(dummy_username, DUMMY_USER_PASSWORD_1)
    users_page.close()

    home_page_logged_out.navigate()

    yield page, dummy_username

    dummy_user_home_logged_out = HomePageLoggedOut(page)
    dummy_user_home_logged_out.navigate()

    home_page_logged_in.navigate(admin_username, admin_password)

    users_page = UsersPage(home_page_logged_in.click_users_tile())
    users_page.remove_user(dummy_username)
    users_page.close()

    home_page_logged_out.navigate()


@pytest.mark.selfservice
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_non_admin_can_change_password(dummy_user_home: Tuple[Page, str]):
    """
    Tests a user can update its password, doing so from the side-menu.

    1. Logs in as the dummy user with its original password.
    2. Changes the password from the side-menu to a new password.
    3. Logs out from the dummy user.
    4. Logs in with the new password.
    """
    page, dummy_username = dummy_user_home
    change_password_page = ChangePasswordDialogPage(page)
    change_password_page.navigate(dummy_username, DUMMY_USER_PASSWORD_1)
    change_password_page.change_password(DUMMY_USER_PASSWORD_1, DUMMY_USER_PASSWORD_2)

    # TODO: This is discouraged, use a different approach
    # NOTE: wait for the password change to occur
    page.wait_for_timeout(5000)

    dummy_user_home_logged_out = HomePageLoggedOut(page)
    dummy_user_home_logged_out.navigate()

    dummy_user_home_logged_in = HomePageLoggedIn(page)
    dummy_user_home_logged_in.navigate(dummy_username, DUMMY_USER_PASSWORD_2)
    dummy_user_home_logged_in.reveal_area(
        dummy_user_home_logged_in.right_side_menu,
        dummy_user_home_logged_in.header.hamburger_icon,
    )
    expect(dummy_user_home_logged_in.right_side_menu.logout_button).to_be_visible()


@pytest.mark.selfservice
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_set_recovery_email(dummy_user_home: Tuple[Page, str]):
    """
    Tests a user can set up a recovery email.

    1. Logs in as the dummy user.
    2. Sets a dummy recovery email from the side-menu.
    3. Logs out from the dummy user.
    4. Logs in again to the dummy user.
    5. Triggers the recovery email window and checks the recovery email is the
    same.
    """
    page, dummy_username = dummy_user_home
    set_recovery_email_page = SetRecoveryEmailDialogPage(page)
    set_recovery_email_page.navigate(dummy_username, DUMMY_USER_PASSWORD_1)
    expect(set_recovery_email_page.submit_button).to_be_visible(timeout=10000)
    set_recovery_email_page.set_recovery_email(DUMMY_EMAIL)

    dummy_user_home_logged_out = HomePageLoggedOut(page)
    dummy_user_home_logged_out.navigate()

    set_recovery_email_page = SetRecoveryEmailDialogPage(page)
    set_recovery_email_page.navigate(dummy_username, DUMMY_USER_PASSWORD_1)
    expect(set_recovery_email_page.submit_button).to_be_visible(timeout=10000)
    expect(set_recovery_email_page.email_box).to_have_value(DUMMY_EMAIL)
    expect(set_recovery_email_page.retype_email_box).to_have_value(DUMMY_EMAIL)


@pytest.mark.selfservice
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_manage_profile(dummy_user_home: Tuple[Page, str]):
    """
    Tests a user can manage their profile.
    1. Logs in as the dummy user.
    2. Sets a description on his profile.
    3. Logs out from the dummy user.
    4. Logs in again to the dummy user.
    5. Checks the description remains the same.
    """
    page, dummy_username = dummy_user_home
    manage_profile_page = ManageProfileDialogPage(page)
    manage_profile_page.navigate(dummy_username, DUMMY_USER_PASSWORD_1)
    expect(manage_profile_page.save_button).to_be_visible()
    manage_profile_page.change_description(DUMMY_DESCRIPTION)

    dummy_user_home_logged_out = HomePageLoggedOut(page)
    dummy_user_home_logged_out.navigate()

    set_recovery_email_page = ManageProfileDialogPage(page)
    set_recovery_email_page.navigate(dummy_username, DUMMY_USER_PASSWORD_1)
    expect(set_recovery_email_page.save_button).to_be_visible(timeout=10000)
    expect(set_recovery_email_page.description_box).to_have_value(DUMMY_DESCRIPTION)


@pytest.mark.selfservice
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_selfservice_portal(navigate_to_selfservice_portal_logged_in):
    """
    Tests the selfservice portal is served and with the correct tiles.

    1. Logs into the portal as a normal user.
    2. Navigates into `/univention/selfservice`.
    3. Checks for the `My profile` and `Protect account` tiles.
    4. Logs out.
    5. Check for `My profile`, `Protect account` and `Password forgotten`
    tiles.
    """
    page = navigate_to_selfservice_portal_logged_in
    selfservice_portal_logged_in = SelfservicePortalLoggedIn(page)
    selfservice_portal_logged_out = SelfservicePortalLoggedOut(page)

    expect(selfservice_portal_logged_in.my_profile_tile).to_be_visible()
    expect(selfservice_portal_logged_in.protect_account_tile).to_be_visible()

    selfservice_portal_logged_out.navigate()
    expect(selfservice_portal_logged_out.my_profile_tile).to_be_visible()
    expect(selfservice_portal_logged_out.protect_account_tile).to_be_visible()
    expect(selfservice_portal_logged_out.password_forgotten_tile).to_be_visible()


def test_admin_invites_new_user_via_email(
        navigate_to_home_page_logged_in_as_admin,
        dummy_username,
        email_test_api,
):
    recovery_email = f'{dummy_username}@external-domain.test'
    page = navigate_to_home_page_logged_in_as_admin
    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_out = HomePageLoggedOut(page)

    users_page = UsersPage(home_page_logged_in.click_users_tile())
    users_page.add_user_button.click()
    users_page.add_user_dialog.add_user(
        username=dummy_username, invite_email=recovery_email)
    users_page.close()

    # TODO: Replace by a retry with timeout or maxretry
    time.sleep(5)

    email = email_test_api.get_one_email(to=recovery_email)

    home_page_logged_out.navigate()

    password_reset_email = PasswordResetEmail(email)
    password_change_page = SetNewPasswordPage(page)
    password_change_page.navigate(url=password_reset_email.link_with_token)
    password_change_page.set_new_password(password=DUMMY_USER_PASSWORD_1)

    # TODO: Replace this with a proper approach, it takes sometimes plenty of
    # time until the login is possible.
    time.sleep(60)

    dummy_user_home_logged_in = HomePageLoggedIn(page)
    dummy_user_home_logged_in.navigate(dummy_username, DUMMY_USER_PASSWORD_1)
    dummy_user_home_logged_in.reveal_area(
        dummy_user_home_logged_in.right_side_menu,
        dummy_user_home_logged_in.header.hamburger_icon,
    )
    expect(dummy_user_home_logged_in.right_side_menu.logout_button).to_be_visible()
