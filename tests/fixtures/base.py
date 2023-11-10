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

from playwright.sync_api import Browser, Page

from umspages.portal.admin_page import AdminPage


@pytest.fixture()
def username(pytestconfig):
    return pytestconfig.option.username


@pytest.fixture()
def password(pytestconfig):
    return pytestconfig.option.password


@pytest.fixture()
def admin_username(pytestconfig):
    return pytestconfig.option.admin_username


@pytest.fixture()
def admin_password(pytestconfig):
    return pytestconfig.option.admin_password


@pytest.fixture()
def portal_base_url(pytestconfig):
    return pytestconfig.option.portal_base_url


@pytest.fixture
def kc_username(pytestconfig):
    return pytestconfig.option.kc_admin_username


@pytest.fixture
def kc_password(pytestconfig):
    return pytestconfig.option.kc_admin_password


@pytest.fixture
def realm(pytestconfig):
    return pytestconfig.option.realm


@pytest.fixture(scope="session")
def keycloak_base_url(pytestconfig):
    return pytestconfig.option.keycloak_base_url


@pytest.fixture
def num_device_block(pytestconfig):
    return pytestconfig.option.num_device_block


@pytest.fixture
def num_ip_block(pytestconfig):
    return pytestconfig.option.num_ip_block


@pytest.fixture(scope="module")
def browser(playwright) -> Browser:
    browser = playwright.chromium.launch(
        headless=False,
        # slow_mo=3000,
    )
    yield browser
    browser.close()


@pytest.fixture()
def main_page(browser, portal_base_url) -> Page:
    context = browser.new_context(
        is_mobile=False,
        # locale='de-DE',
        locale='en-EN',
        timezone_id='Europe/Berlin',
    )
    page = context.new_page()
    page.goto(portal_base_url)
    page.wait_for_load_state("load")
    yield page
    page.close()


@pytest.fixture(scope="function")
def login_page(browser, portal_base_url) -> Page:
    context = browser.new_context(
        is_mobile=False,
        locale='en-EN',
        # locale='de-DE',
        timezone_id='Europe/Berlin',
    )
    page = context.new_page()
    # page.goto(portal_base_url + '/univention/login')
    page.goto(portal_base_url + '/univention/login?location=/univention/portal')
    page.wait_for_load_state("load")
    yield LoginPage(page)
    page.close()


@pytest.fixture()
def admin_page(
        login_page,
        admin_username,
        admin_password
) -> AdminPage:
    page = login_page
    page.locator('#umcLoginUsername').fill(admin_username)
    page.locator('#umcLoginPassword').fill(admin_password)
    page.locator('#umcLoginForm').locator('.umcLoginFormButton').click()
    page.wait_for_url("**/univention/portal/#/")
    yield AdminPage(page)
    page.close()


@pytest.fixture()
def user_page(
        login_page : LoginPage,
        username,
        password
) -> Page:
    page = login_page
    page.locator('#umcLoginUsername').fill(username)
    page.locator('#umcLoginPassword').fill(password)
    page.locator('#umcLoginForm').locator('.umcLoginFormButton').click()
    page.wait_for_url("**/univention/portal/#/")
    yield page
    page.close()
