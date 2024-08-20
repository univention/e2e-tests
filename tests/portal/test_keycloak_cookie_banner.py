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
import json
from umspages.common.base import expect
from umspages.portal.login_page import LoginPage


@pytest.fixture
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "storage_state": {
            "cookies": [],
            "origins": [],
        },
    }


@pytest.mark.cookie_banner
@pytest.mark.portal
@pytest.mark.acceptance_environment
@pytest.mark.parametrize("show_banner, expected_visibility", [
    (True, "visible"),
    (False, "hidden")
])
def test_cookie_banner(page, show_banner, expected_visibility):
    """Tests the presence/absence and content of the cookie banner"""
    # Mock the request to meta.json
    page.route(
        "**/univention/meta.json",
        lambda route: route.fulfill(
            status=200,
            body=json.dumps(
                {
                    "administrator": "Administrator",
                    "cookieBanner": {
                        "cookie": None,
                        "domains": [],
                        "show": show_banner,
                        "text": {
                            "de": 'Test cookie banner message DE',
                            "en": 'Test cookie banner message EN',
                        },
                        "title": {"de": "Test Cookie Setting DE", "en": "Test Cookie Settings EN"},
                    },
                }
            ),
        ),
    )

    login_page = LoginPage(page)
    login_page.navigate()
    cookie_banner = page.locator(".cookie-banner .dialog")

    if expected_visibility == "visible":
        expect(cookie_banner).to_be_visible()
        expect(cookie_banner).to_have_text(
            "Test Cookie Settings EN\nTest cookie banner message EN\nACCEPT",
            use_inner_text=True,
        )
        button = page.locator("button.cookie-banner-button")
        expect(button).to_have_text("Accept")
        button.click()
        expect(cookie_banner).to_be_hidden()
    else:
        expect(cookie_banner).to_be_hidden()
