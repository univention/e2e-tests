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

import pytest
from playwright.sync_api import Page

from e2e.decorators import retrying
from e2e.email.password_reset import PasswordResetEmail
from umspages.common.base import expect
from umspages.portal.home_page.logged_in import HomePageLoggedIn
from umspages.portal.home_page.logged_out import HomePageLoggedOut
from umspages.portal.login_page import LoginPage
from umspages.portal.selfservice.base import SelfservicePortal
from umspages.portal.selfservice.change_password import ChangePasswordDialogPage
from umspages.portal.selfservice.manage_profile import ManageProfileDialogPage
from umspages.portal.selfservice.password_forgotten import PasswordForgottenPage
from umspages.portal.selfservice.set_new_password import SetNewPasswordPage
from umspages.portal.selfservice.set_recovery_email import SetRecoveryEmailDialogPage
from umspages.portal.users.users_page import UsersPage

from tests.portal.conftest import WaitForPortalSync

DUMMY_USER_PASSWORD_2 = "secondpass"
DUMMY_EMAIL = "mail@example.org"
DUMMY_DESCRIPTION = "some description"


@pytest.fixture()
def dummy_username():
    yield f"dummy_{random.randint(1000, 9999)}"  # noqa: S311


@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_portal_tiles_and_central_navigation_update(user, wait_for_portal_sync: WaitForPortalSync):
    """
    Prerequisite for all other selfservice tests.
    If the portal-consumer does not work, nothing else will either.
    """
    username = user.properties["username"]
    wait_for_portal_sync(username, 4)


@pytest.mark.selfservice
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_user_changes_password_via_side_menu(
    navigate_to_login_page: Page,
    user,
    user_password: str,
    wait_for_portal_sync: WaitForPortalSync,
    wait_for_ldap_secondaries_to_catch_up,
):
    username = user.properties["username"]
    wait_for_portal_sync(username, 4)

    page = navigate_to_login_page
    change_password_page = ChangePasswordDialogPage(page)
    change_password_page.navigate(username, user_password)
    change_password_page.change_password(user_password, DUMMY_USER_PASSWORD_2)
    wait_for_ldap_secondaries_to_catch_up()

    dummy_user_home_logged_out = HomePageLoggedOut(page)
    dummy_user_home_logged_out.navigate()

    assert_user_can_log_in(page, username, DUMMY_USER_PASSWORD_2)


@pytest.mark.selfservice
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_set_recovery_email(user, user_password, wait_for_portal_sync: WaitForPortalSync, page):
    """
    Tests a user can set up a recovery email.

    1. Logs in as the dummy user.
    2. Sets a dummy recovery email from the side-menu.
    3. Logs out from the dummy user.
    4. Logs in again to the dummy user.
    5. Triggers the recovery email window and checks the recovery email is the
    same.
    """
    username = user.properties["username"]
    wait_for_portal_sync(username, 4)

    set_recovery_email_page = SetRecoveryEmailDialogPage(page)
    set_recovery_email_page.navigate(username, user_password)
    expect(set_recovery_email_page.submit_button).to_be_visible(timeout=10000)
    set_recovery_email_page.set_recovery_email(DUMMY_EMAIL)

    dummy_user_home_logged_out = HomePageLoggedOut(page)
    dummy_user_home_logged_out.navigate()

    set_recovery_email_page = SetRecoveryEmailDialogPage(page)
    set_recovery_email_page.navigate(username, user_password)
    expect(set_recovery_email_page.submit_button).to_be_visible(timeout=10000)
    expect(set_recovery_email_page.email_box).to_have_value(DUMMY_EMAIL)
    expect(set_recovery_email_page.retype_email_box).to_have_value(DUMMY_EMAIL)


@pytest.mark.selfservice
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_manage_profile(user, user_password, wait_for_portal_sync: WaitForPortalSync, page):
    """
    Tests a user can manage their profile.
    1. Logs in as the dummy user.
    2. Sets a description on his profile.
    3. Logs out from the dummy user.
    4. Logs in again to the dummy user.
    5. Checks the description remains the same.
    """
    username = user.properties["username"]
    wait_for_portal_sync(username, 4)

    manage_profile_page = ManageProfileDialogPage(page)
    manage_profile_page.navigate(username, user_password)
    expect(manage_profile_page.save_button).to_be_visible()
    manage_profile_page.change_description(DUMMY_DESCRIPTION)

    dummy_user_home_logged_out = HomePageLoggedOut(page)
    dummy_user_home_logged_out.navigate()

    set_recovery_email_page = ManageProfileDialogPage(page)
    set_recovery_email_page.navigate(username, user_password)
    expect(set_recovery_email_page.save_button).to_be_visible(timeout=10000)
    expect(set_recovery_email_page.description_box).to_have_value(DUMMY_DESCRIPTION)


@pytest.mark.selfservice
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_admin_sees_correct_tiles_in_selfservice_portal(page, admin_username, admin_password):
    selfservice_portal = SelfservicePortal(page)
    selfservice_portal.navigate()
    selfservice_portal.login(admin_username, admin_password)

    expect(selfservice_portal.my_profile_tile).to_be_visible()
    expect(selfservice_portal.protect_account_tile).to_be_visible()


@pytest.mark.selfservice
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_admin_does_not_see_umc_tiles_in_selfservice_portal(page, admin_username, admin_password):
    selfservice_portal = SelfservicePortal(page)
    selfservice_portal.navigate()
    selfservice_portal.login(admin_username, admin_password)

    expect(selfservice_portal.tiles.first).to_be_visible()
    expect(selfservice_portal.umc_tiles_headline).not_to_be_visible()


@pytest.mark.selfservice
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_user_sees_correct_tiles_in_selfservice_portal(page, user, user_password, wait_for_portal_sync):
    username = user.properties["username"]
    wait_for_portal_sync(username, 4)

    selfservice_portal = SelfservicePortal(page)
    selfservice_portal.navigate()
    selfservice_portal.login(username, user_password)

    expect(selfservice_portal.my_profile_tile).to_be_visible()
    expect(selfservice_portal.protect_account_tile).to_be_visible()


@pytest.mark.selfservice
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_anonymous_sees_correct_tiles_in_selfservice_portal(page):
    selfservice_portal = SelfservicePortal(page)
    selfservice_portal.navigate()

    expect(selfservice_portal.my_profile_tile).to_be_visible()
    expect(selfservice_portal.protect_account_tile).to_be_visible()
    expect(selfservice_portal.password_forgotten_tile).to_be_visible()


@pytest.mark.selfservice
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_admin_invites_new_user_via_email(
    navigate_to_home_page_logged_in_as_admin,
    dummy_username,
    user_password,
    email_test_api,
    wait_for_ldap_secondaries_to_catch_up,
):
    page = navigate_to_home_page_logged_in_as_admin
    set_new_password_page = SetNewPasswordPage(page)
    recovery_email = f"{dummy_username}@external-domain.test"

    create_user_via_ui_with_email_invitation(page, dummy_username, recovery_email)
    password_reset_link = get_password_reset_link_with_token(email_test_api, recovery_email)
    set_new_password_page.navigate(url=password_reset_link)
    set_new_password_page.set_new_password(password=user_password)
    expect(set_new_password_page.password_change_successful_dialog).to_be_visible()
    wait_for_ldap_secondaries_to_catch_up()

    assert_user_can_log_in(page, dummy_username, user_password)


def get_password_reset_link_with_token(email_test_api, recovery_email):
    email = retrying(email_test_api.get_one_email)(to=recovery_email)
    password_reset_email = PasswordResetEmail(email)
    return password_reset_email.link_with_token


def create_user_via_ui_with_email_invitation(page, dummy_username, recovery_email):
    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_out = HomePageLoggedOut(page)

    users_page = UsersPage(home_page_logged_in.click_users_tile())
    users_page.add_user_button.click()
    users_page.add_user_dialog.add_user(username=dummy_username, invite_email=recovery_email)
    users_page.close()
    home_page_logged_out.navigate()


def assert_user_can_log_in(page, admin_username, admin_password):
    dummy_user_home_logged_in = HomePageLoggedIn(page)
    dummy_user_home_logged_in.navigate(admin_username, admin_password)
    dummy_user_home_logged_in.reveal_area(
        dummy_user_home_logged_in.right_side_menu,
        dummy_user_home_logged_in.header.hamburger_icon,
    )
    expect(dummy_user_home_logged_in.right_side_menu.logout_button).to_be_visible()


@pytest.mark.selfservice
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_user_requests_password_forgotten_link_from_login_page(
    page,
    user,
    email_test_api,
    faker,
    subtests,
    wait_for_ldap_secondaries_to_catch_up,
):
    login_page = LoginPage(page)
    login_page.navigate(cookies_accepted=True)
    login_page.forgot_password_link.click()

    request_token_via_email(page, user)
    assert_token_request_was_successful(page, subtests)

    link_with_token = get_password_reset_link_with_token(email_test_api, user.properties["PasswordRecoveryEmail"])
    assert link_with_token

    new_password = faker.password()
    set_new_password(page, new_password, link_with_token)
    wait_for_ldap_secondaries_to_catch_up()
    assert_password_change_is_successful(page, subtests, user, new_password)


@pytest.mark.selfservice
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_user_requests_password_forgotten_via_selfservice_portal(
    page,
    user,
    email_test_api,
    faker,
    subtests,
    wait_for_ldap_secondaries_to_catch_up,
):
    selfservice_portal = SelfservicePortal(page)
    selfservice_portal.navigate()
    selfservice_portal.password_forgotten_tile.click()

    request_token_via_email(page, user)
    assert_token_request_was_successful(page, subtests)

    link_with_token = get_password_reset_link_with_token(email_test_api, user.properties["PasswordRecoveryEmail"])
    assert link_with_token

    new_password = faker.password()
    set_new_password(page, new_password, link_with_token)
    wait_for_ldap_secondaries_to_catch_up()
    assert_password_change_is_successful(page, subtests, user, new_password)


def request_token_via_email(page, user):
    password_forgotten_page = PasswordForgottenPage(page)
    password_forgotten_page.request_token_via_email(user.properties["username"])


def assert_token_request_was_successful(page, subtests):
    password_forgotten_page = PasswordForgottenPage(page)
    with subtests.test(msg="Notification popup is visible"):
        expect(password_forgotten_page.popup_notification_container).to_be_visible()

    with subtests.test(msg="Notification contains success message"):
        notification = password_forgotten_page.popup_notification_container.notification(0)
        expect(notification).to_contain_text("Successfully sent Token")

    with subtests.test(msg="Set new password page is displayed"):
        set_new_password_page = SetNewPasswordPage(page)
        assert set_new_password_page.is_displayed()


def set_new_password(page, new_password, link_with_token):
    page.goto(link_with_token)
    set_new_password_page = SetNewPasswordPage(page)
    set_new_password_page.set_new_password(password=new_password)


def assert_password_change_is_successful(page, subtests, user, new_password):
    set_new_password_page = SetNewPasswordPage(page)
    with subtests.test(msg="Password change is confirmed in UI"):
        expect(set_new_password_page.password_change_successful_dialog).to_be_visible()

    with subtests.test(msg="Login with new password is possible"):
        assert_user_can_log_in(page, user.properties["username"], new_password)


@pytest.mark.selfservice
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_user_forced_to_change_password_on_next_login(
    user_password,
    user,
    faker,
    page,
    wait_for_ldap_secondaries_to_catch_up,
    wait_for_portal_sync: WaitForPortalSync,
):
    username = user.properties["username"]

    user.properties["pwdChangeNextLogin"] = True
    user.save()
    wait_for_ldap_secondaries_to_catch_up()
    wait_for_portal_sync(username, 4)

    home_page_logged_out = HomePageLoggedOut(page)

    # Log out admin
    home_page_logged_out.navigate()

    # Log in as the new user
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(username, user_password)

    # Change password
    new_password = faker.password()
    page.get_by_label("Password", exact=True).fill(user_password)
    page.get_by_label("New Password").fill(new_password)
    page.get_by_label("Confirm password").fill(new_password)
    page.get_by_role("button", name="Submit").click()
    wait_for_ldap_secondaries_to_catch_up()

    # Expect to be redirected to the portal home page
    home_page_logged_in = HomePageLoggedIn(page)
    expect(home_page_logged_in.header.hamburger_icon).to_be_visible()

    # Log out
    home_page_logged_in.logout()
    time.sleep(0.1)

    # Try to log in with old password (should fail)
    login_page.navigate()
    login_page.login(username, user_password)
    expect(home_page_logged_in.header.hamburger_icon).not_to_be_visible()

    # Log in with new password (should succeed)
    login_page.login(username, new_password)
    expect(home_page_logged_in.header.hamburger_icon).to_be_visible()
