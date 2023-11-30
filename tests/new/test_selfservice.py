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

import pytest
from playwright.sync_api import expect

from pom.home_user_page import AdminHomePage
from pom.manage_users_page import ManageUsersPage

test_user_1 = {
    'title': 'Mr.',
    'first_name': 'test_user_1',
    'last_name': 'test_user_1_last_name',
    'user_name': 'tu1',
    'email': 'test_user_1@test_email.com',
    'password': 'SWPtester',
}

test_user_2 = {
    'title': 'Mr.',
    'first_name': 'test_user_2',
    'last_name': 'test_user_2_last_name',
    'user_name': 'tu2',
    'email': 'test_user_2@test_email.com',
    'password': 'SWPtester',
}

@pytest.mark.devenv
@pytest.mark.gaia
class TestSelfService:

    @pytest.mark.dependency()
    def test_that_test_user_is_absent(self):
        pass

    @pytest.mark.dependency(depends=['test_that_test_user_is_absent'])
    def test_add_dummy_user(
            self,
            localization: dict,
            admin_home_page: AdminHomePage,
    ):
        page = admin_home_page
        with page._page.expect_popup() as popup_info:
            page.user_widget.click()
            popup_info.value.wait_for_load_state()
            users_page = ManageUsersPage(popup_info.value)
            users_page.add_user('openDesk User', test_user_1)
            users_page._page.close()

        with page._page.expect_popup() as popup_info:
            page.user_widget.click()
            popup_info.value.wait_for_load_state()
            users_page = ManageUsersPage(popup_info.value)
            users_page.add_user('openDesk User', test_user_2)
            users_page._page.close()

    @pytest.mark.dependency(depends=['test_add_user'])
    def test_that_dummy_users_exist(self):
        pass

    @pytest.mark.dependency(depends=['test_that_test_users_exist'])
    def test_change_dummy_user_password(self):
        pass

    @pytest.mark.dependency(depends=['test_change_user_password'])
    def test_login_user_with_new_password(self):
        pass

    @pytest.mark.dependency(depends=['test_login_user_with_new_password'])
    def test_remove_dummy_users(self):
        pass

    '''
    def test_remove_user(
            self,
            localization: dict,
            admin_home_page: GaiaAdminHomePage,
    ):
        page = admin_home_page
        with page._page.expect_popup() as popup_info:
            page.user_widget.click()
            users_page = popup_info.value
            users_page.wait_for_load_state()
            users_page.close()

    def test_get_users(
            self,
            localization: dict,
            admin_home_page: GaiaAdminHomePage,
    ):
        page = admin_home_page
        with page._page.expect_popup() as popup_info:
            page.user_widget.click()
            users_page = popup_info.value
            users_page.wait_for_load_state()
            users_page.close()

    def test_search_users(
            self,
            localization: dict,
            admin_home_page: GaiaAdminHomePage,
    ):
        page = admin_home_page
        with page._page.expect_popup() as popup_info:
            page.user_widget.click()
            users_page = popup_info.value
            users_page.wait_for_load_state()
            users_page.close()
    '''

'''
import random

import pytest
from playwright.sync_api import Page
from umspages.common.base import expect
from umspages.portal.home_page.logged_in import HomePageLoggedIn
from umspages.portal.home_page.logged_out import HomePageLoggedOut
from umspages.portal.selfservice.change_password import ChangePasswordDialogPage
from umspages.portal.users.users_page import UsersPage


DUMMY_USER_NAME = f"dummy_{random.randint(1000,9999)}"  # noqa: S311
DUMMY_USER_PASSWORD_1 = "firstpass"
DUMMY_USER_PASSWORD_2 = "secondpass"


@pytest.fixture()
def dummy_user_home(navigate_to_home_page_logged_in: Page, username, password) -> Page:
    page = navigate_to_home_page_logged_in
    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_out = HomePageLoggedOut(page)

    with page.expect_popup() as popup_info:
        home_page_logged_in.click_users_tile()
        popup = popup_info.value

    popup.wait_for_load_state()
    users_page = UsersPage(popup)
    users_page.add_user(DUMMY_USER_NAME, DUMMY_USER_PASSWORD_1)
    popup.close()

    home_page_logged_out.navigate()

    yield page

    dummy_user_home_logged_out = HomePageLoggedOut(page)
    dummy_user_home_logged_out.navigate()

    home_page_logged_in.navigate(username, password)

    with page.expect_popup() as popup_info:
        home_page_logged_in.click_users_tile()
        popup = popup_info.value

    popup.wait_for_load_state()
    users_page = UsersPage(popup)
    users_page.remove_user(DUMMY_USER_NAME)
    popup.close()

    home_page_logged_out.navigate()


def test_non_admin_can_change_password(dummy_user_home: Page):
    change_password_page = ChangePasswordDialogPage(dummy_user_home)
    change_password_page.navigate(DUMMY_USER_NAME, DUMMY_USER_PASSWORD_1)
    change_password_page.change_password(DUMMY_USER_PASSWORD_1, DUMMY_USER_PASSWORD_2)

    dummy_user_home_logged_out = HomePageLoggedOut(dummy_user_home)
    dummy_user_home_logged_out.navigate()

    dummy_user_home_logged_in = HomePageLoggedIn(dummy_user_home)
    dummy_user_home_logged_in.navigate(DUMMY_USER_NAME, DUMMY_USER_PASSWORD_2)
    dummy_user_home_logged_in.reveal_area(
        dummy_user_home_logged_in.right_side_menu,
        dummy_user_home_logged_in.header.hamburger_icon,
    )
    expect(dummy_user_home_logged_in.right_side_menu.logout_button).to_be_visible()
'''
