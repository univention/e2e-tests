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

from umspages.portal.home_page.logged_in import HomePageLoggedIn
from umspages.portal.home_page.logged_out import HomePageLoggedOut
from umspages.portal.login_page import LoginPage
from umspages.portal.main_page import MainPage


@pytest.fixture(scope="session")
def username(pytestconfig):
    return pytestconfig.option.username


@pytest.fixture(scope="session")
def password(pytestconfig):
    return pytestconfig.option.password


@pytest.fixture(scope="session")
def admin_username(pytestconfig):
    return pytestconfig.option.admin_username


@pytest.fixture(scope="session")
def admin_password(pytestconfig):
    return pytestconfig.option.admin_password


@pytest.fixture(scope="session")
def portal_base_url(pytestconfig):
    return pytestconfig.getoption("--portal-base-url")


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, portal_base_url):
    browser_context_args["base_url"] = portal_base_url
    return browser_context_args


@pytest.fixture()
def navigate_to_home_page_logged_out(page):
    home_page_logged_out = HomePageLoggedOut(page)
    home_page_logged_out.navigate()
    return page


@pytest.fixture()
def navigate_to_login_page(page):
    login_page = LoginPage(page)
    login_page.navigate()
    return page


@pytest.fixture()
def navigate_to_saml_login_page(page):
    login_page = LoginPage(page)
    login_page.navigate_saml()
    return page


@pytest.fixture()
def navigate_to_home_page_logged_in(page, username, password):
    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_in.navigate(username, password)
    return page


@pytest.fixture()
def navigate_to_home_page_logged_in_as_admin(page, admin_username, admin_password):
    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_in.navigate(admin_username, admin_password)
    return page


@pytest.fixture(scope="module")
def browser(pytestconfig, playwright) -> Browser:
    browser = playwright[
        pytestconfig.getoption("--browser_name")
    ].launch(
        headless=(not pytestconfig.getoption("--headed")),
        slow_mo=pytestconfig.getoption("--slow-mo"),
    )
    yield browser
    browser.close()


@pytest.fixture()
def main_page(pytestconfig, browser, portal_base_url) -> MainPage:
    context = browser.new_context(
        is_mobile=pytestconfig.getoption("--is-mobile"),
        locale=pytestconfig.getoption("--locale"),
        timezone_id=pytestconfig.getoption("--time-zone"),
    )
    page = context.new_page()
    page.goto(portal_base_url)
    page.wait_for_load_state("load")
    yield MainPage(page)
    page.close()


@pytest.fixture()
def login_page(pytestconfig, main_page) -> LoginPage:
    main_page.login_widget.click()
    main_page.page.wait_for_url("**/univention/login**")
    yield LoginPage(main_page.page)
    '''
    context = browser.new_context(
        is_mobile=pytestconfig.getoption("--is-mobile"),
        locale=pytestconfig.getoption("--locale"),
        timezone_id=pytestconfig.getoption("--time-zone"),
    )
    page = context.new_page()
    page.goto(portal_base_url)
    page.wait_for_load_state("load")
    yield MainPage(page)
    page.close()
    '''
