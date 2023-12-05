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

import pytest
from playwright.sync_api import Page

from umspages.common.base import expect
from umspages.portal.home_page.logged_in import HomePageLoggedIn
from umspages.portal.home_page.logged_out import HomePageLoggedOut
from umspages.portal.selfservice.change_password import \
    ChangePasswordDialogPage
from umspages.portal.selfservice.logged_in import SelfservicePortalLoggedIn
from umspages.portal.selfservice.logged_out import SelfservicePortalLoggedOut
from umspages.portal.users.users_page import UsersPage

DUMMY_USER_NAME = f"dummy_{random.randint(1000, 9999)}"  # noqa: S311
DUMMY_USER_PASSWORD_1 = "firstpass"
DUMMY_USER_PASSWORD_2 = "secondpass"


@pytest.fixture()
def dummy_user_home(
    navigate_to_home_page_logged_in_as_admin: Page, admin_username, admin_password
) -> Page:
    page = navigate_to_home_page_logged_in_as_admin
    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_out = HomePageLoggedOut(page)

    users_page = UsersPage(home_page_logged_in.click_users_tile())
    users_page.add_user(DUMMY_USER_NAME, DUMMY_USER_PASSWORD_1)
    users_page.close()

    home_page_logged_out.navigate()

    yield page

    dummy_user_home_logged_out = HomePageLoggedOut(page)
    dummy_user_home_logged_out.navigate()

    home_page_logged_in.navigate(admin_username, admin_password)

    users_page = UsersPage(home_page_logged_in.click_users_tile())
    users_page.remove_user(DUMMY_USER_NAME)
    users_page.close()

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


def test_selfservice_portal(navigate_to_selfservice_portal_logged_in):
    page = navigate_to_selfservice_portal_logged_in
    selfservice_portal_logged_in = SelfservicePortalLoggedIn(page)
    selfservice_portal_logged_out = SelfservicePortalLoggedOut(page)

    expect(selfservice_portal_logged_in.my_profile_tile).to_be_visible()
    expect(selfservice_portal_logged_in.protect_account_tile).to_be_visible()

    selfservice_portal_logged_out.navigate()
    expect(selfservice_portal_logged_out.my_profile_tile).to_be_visible()
    expect(selfservice_portal_logged_out.protect_account_tile).to_be_visible()
    expect(selfservice_portal_logged_out.password_forgotten_tile).to_be_visible()
