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


def test_portal_login_page_design(login_page):

    # Check main elements
    expect(login_page).to_have_title('Univention Login')
    expect(login_page.locator('#umcLoginUsername')).to_be_visible()
    expect(login_page.locator('#umcLoginPassword')).to_be_visible()
    expect(login_page.locator('#umcLoginForm').locator('.umcLoginFormButton')).to_be_visible()
    expect(login_page.get_by_role('link', name='How do I login?')).to_be_visible()

    # Check right side menu
    menu = login_page.locator('span[widgetid="umc_menu_Button_0"]')
    expect(menu).to_be_visible()


def test_portal_login_page_lang_en(login_page):
    page = login_page
    # assert 'en' == page.locator("html").get_attribute("lang")
    assert page.locator('.umcHeaderLeft').locator('h2', has_text='UCS')
    assert page.locator('#umcLoginContent').locator('h2', has_text='Login at null')
    assert page.locator('#umcLoginForm').locator('#umcLoginUsernameLabel', has_text='Username')
    assert page.locator('#umcLoginForm').locator('#umcLoginPasswordLabel', has_text='Password')
    assert page.locator('#umcLoginForm').locator('.umcLoginFormButton', has_text='Login')
    assert page.locator('#umcLoginLinks', has_text='How do I login?')


def test_portal_login_page_lang_de(login_page):
    """
    TODO
    """
    pass


def test_portal_login_page_login_button(login_page, username, password):
    login_page.locator('#umcLoginUsername').fill(username)
    login_page.locator('#umcLoginPassword').fill(password)
    login_page.locator('#umcLoginForm').locator('.umcLoginFormButton').click()
    expect(login_page).to_have_title('Univention Management Console')