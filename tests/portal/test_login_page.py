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

from umspages.portal.home_page.logged_in import HomePageLoggedIn
from umspages.portal.home_page.logged_out import HomePageLoggedOut
from umspages.portal.login_page import LoginPage


def test_portal_login_page_design(
        login_page: LoginPage,
        localization: dict,
):
    page = login_page

    assert page.title == 'Univention Login'

    expect(page.username_input).to_be_visible()
    expect(page.password_input).to_be_visible()
    expect(page.login_button).to_be_visible()
    expect(page.menu).to_be_visible()
    expect(page.help_button).to_be_visible()
    expect(page.back_button).to_be_visible()

    # Check localization
    loc = localization
    # There is not implemented attribute 'lang'
    # on the page
    # assert page.lang == loc.lang

    loc = loc.login_page
    assert page.header == loc.PAGE_HEADER
    assert page.login_title == loc.LOGIN_FORM_TITLE
    assert page.username_input_label == loc.USERNAME_INPUT_LABEL
    assert page.password_input_label == loc.PASSWORD_INPUT_LABEL
    assert page.login_button_label == loc.LOGIN_BUTTON_LABEL
    # assert page.help_button.inner_text() == loc.MENU_HELP_LABEL
    assert page.back_button.inner_text() == loc.MENU_BACK_BUTTON


def test_portal_login_page_login(
        login_page,
        username,
        password
):
    login_page.username_input.fill(username)
    login_page.password_input.fill(password)
    login_page.login_button.click()
    login_page.page.wait_for_url("**/univention/portal/#/")
    expect(login_page.page).to_have_title('Sovereign Workplace')


def test_portal_login_page_login_saml(
        login_page,
        username,
        password
):
    '''
    TODO
    '''
    pass
