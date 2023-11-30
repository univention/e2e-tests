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
from pom.home_user_page import (AdminHomePage,
                                UserHomePage,
                                HomePage)
from pom.login_page import (DevenvLoginPage, GaiaLoginPage,
                                        LoginPage)
from pom.main_page import MainPage
from pom.udm import UDMSession


@pytest.fixture()
def udm_session(udm_rest_api_base_url, udm_admin_username, udm_admin_password):
    return UDMSession(
        udm_rest_api_base_url,
        udm_admin_username,
        udm_admin_password,
    )


@pytest.fixture(scope="module")
def browser(
        pytestconfig,
        playwright
) -> Browser:
    browser_name = pytestconfig.getoption("--browser")
    browser = playwright[browser_name[0] if browser_name else "chromium"].launch(
        headless=(not pytestconfig.getoption("--headed")),
        slow_mo=pytestconfig.getoption("--slowmo"),
    )
    yield browser
    browser.close()


@pytest.fixture()
def main_page(
        pytestconfig,
        cluster,
        browser,
        portal_base_url
) -> MainPage:
    context = browser.new_context(
        is_mobile=pytestconfig.getoption("--is-mobile"),
        locale=pytestconfig.getoption("--locale"),
        timezone_id=pytestconfig.getoption("--time-zone"),
    )
    page = context.new_page()
    page.goto(portal_base_url + '/univention/portal/#/', wait_until='load')
    page.wait_for_load_state("load")
    mp = MainPage(page)
    mp.accept_cookie()
    yield mp
    page.close()


@pytest.fixture()
def login_page(
        cluster,
        main_page: MainPage
) -> LoginPage:
    main_page.login_widget.click()
    page = main_page._page

    if cluster == "gaia":
        lp = GaiaLoginPage(page)
    else:
        lp = DevenvLoginPage(page)

    yield lp
    page.close()


@pytest.fixture()
def user_home_page(
        cluster,
        login_page: LoginPage,
        username, password
) -> HomePage:
    login_page.login(username, password)
    yield UserHomePage(login_page._page)
    login_page._page.close()


@pytest.fixture()
def admin_home_page(
        cluster,
        login_page: LoginPage,
        admin_username, admin_password
) -> HomePage:
    login_page.login(admin_username, admin_password)
    yield AdminHomePage(login_page._page)
    login_page._page.close()
