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

from pathlib import Path

import pytest
from playwright.sync_api import expect

from umspages.portal.login_page import LoginPage

SCREENSHOT_SIZE = [
    (1920, 1080),
]

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


@pytest.mark.screenshots
@pytest.mark.parametrize(
    "screenshot_page", [viewport_size_for_screenshots_1280_720, viewport_size_for_screenshots_1920_1080], indirect=True
)
class TestScreenshotsBase(object):
    @pytest.mark.parametrize("screenshot_language", ["English", "Deutsch"])
    def test_login_form(self, screenshot_page, screenshots_output_dir, screenshot_language, request):
        login_page = LoginPage(screenshot_page)
        if screenshot_language != "English":
            login_page.switch_language(screenshot_language)
        login_page.navigate()
        page = login_page.page
        # expect(page.get_by_label("Username")).to_be_visible()
        page.screenshot(path=screenshot_filename(request, screenshots_output_dir))

    def test_login_form_box(self, screenshot_page, screenshots_output_dir, request):
        login_page = LoginPage(screenshot_page)
        login_page.navigate()
        page = login_page.page
        expect(page.get_by_label("Username")).to_be_visible()
        login_box = page.get_by_text("English English German (Deutsch) Sign in to your account Username or email")
        login_box.screenshot(path=screenshot_filename(request, screenshots_output_dir, prefix="box-"))
