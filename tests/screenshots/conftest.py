# Like what you see? Join us!
# https://www.univention.com/about-us/careers/vacancies/
#
# Copyright 2001-2025 Univention GmbH
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

from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse

import pytest

SCREENSHOT_NAME_REPLACEMENTS = str.maketrans(
    {
        "[": "--",
        "]": "",
        "/": "-",
    }
)


def screenshot_filename(request, screenshots_output_dir, prefix: str = "") -> Path:
    filename = request.node.name.translate(SCREENSHOT_NAME_REPLACEMENTS)
    return Path(screenshots_output_dir, f"{prefix}{filename}.png")


def set_viewport_size(page, width=1920, height=1080):
    page.set_viewport_size({"width": width, "height": height})
    return page


def viewport_size_for_screenshots_1920_1080(page):
    set_viewport_size(page)
    return page


def viewport_size_for_screenshots_1280_720(page):
    set_viewport_size(page, 1280, 720)
    return page


@pytest.fixture
def screenshot_page(request, page):
    page = request.param(page)
    return page


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, portal_base_url, keycloak_base_url):
    in_a_week = datetime.now() + timedelta(weeks=1)
    portal_cookie_domain = urlparse(portal_base_url).hostname
    keycloak_cookie_domain = urlparse(keycloak_base_url).hostname
    return {
        **browser_context_args,
        "base_url": portal_base_url,
        "locale": "en-US",
        "timezone_id": "Europe/Berlin",
        "storage_state": {
            # This is a slight violation of good end-to-end testing practices.
            # Nearly all of our tests want to check the system with the cookie
            # consent already given. This violation does make each of those
            # tests simpler.
            #
            # Tests which explicitly need fresh cookies can use e.g.
            # `pytest.mark.browser_context_args` or define this fixture in a
            # smaller scope to adjust things.
            "cookies": [
                {
                    "domain": f".{keycloak_cookie_domain}",
                    "expires": in_a_week.timestamp(),
                    "httpOnly": False,
                    "name": "univentionCookieSettingsAccepted",
                    "path": "/",
                    "sameSite": "Strict",
                    "secure": False,
                    "value": "do-not-change-me",
                },
                {
                    "domain": f".{portal_cookie_domain}",
                    "expires": in_a_week.timestamp(),
                    "httpOnly": False,
                    "name": "univentionCookieSettingsAccepted",
                    "path": "/",
                    "sameSite": "Strict",
                    "secure": False,
                    "value": "do-not-change-me",
                },
            ],
            "origins": [],
        },
    }
