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

from umspages.portal.home_page.logged_in import HomePageLoggedIn
from umspages.portal.login_page import LoginPage


@pytest.fixture(scope="module")
def logged_in_cookies(browser, browser_context_args, username, password):
    context = browser.new_context(**browser_context_args)
    page = context.new_page()

    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(username, password)

    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_in.assert_logged_in()

    cookies = page.context.cookies()
    return cookies


@pytest.mark.cookies
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_cookie_hardening_sets_samesite(logged_in_cookies):
    umc_session_cookie = _get_cookie(logged_in_cookies, "UMCSessionId")
    assert umc_session_cookie["sameSite"] == "Strict"


@pytest.mark.cookies
@pytest.mark.portal
@pytest.mark.acceptance_environment
def test_cookie_hardening_sets_secure(logged_in_cookies):
    umc_session_cookie = _get_cookie(logged_in_cookies, "UMCSessionId")
    assert umc_session_cookie["secure"] == True


@pytest.mark.cookies
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_cookie_hardening_does_not_set_expires(logged_in_cookies):
    umc_session_cookie = _get_cookie(logged_in_cookies, "UMCSessionId")
    assert umc_session_cookie["expires"] == -1


def _get_cookie(cookies, name):
    return [c for c in cookies if c["name"] == name][0]
