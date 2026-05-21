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

from umspages.portal.login_page import LoginPage

from .conftest import (
    SCREENSHOT_NAME_REPLACEMENTS,
    switch_language,
    viewport_size_for_screenshots_1280_720,
    viewport_size_for_screenshots_1920_1080,
)

PORTAL_SCREENSHOTS = [
    pytest.param("", None, id="language_en"),
    pytest.param("-de", "Deutsch", id="language_de"),
]

LOGIN_FORM_SCREENSHOTS = [
    pytest.param("", None, id="language_en"),
    pytest.param("-de", "German (Deutsch)", id="language_de"),
]

LOGIN_BOX_SCREENSHOTS = [
    pytest.param(
        "",
        None,
        "English English German (Deutsch) Sign in to your account Username or email",
        id="language_en",
    ),
    pytest.param(
        "-de",
        "German (Deutsch)",
        "Deutsch Deutsch Englisch (English) Bei Ihrem Konto anmelden Benutzername oder E",
        id="language_de",
    ),
]

LANGUAGE_PARAM_IDS = ("language_en", "language_de")


def screenshot_filename(request, screenshots_output_dir, prefix: str = "", suffix: str = "") -> Path:
    filename = request.node.name.translate(SCREENSHOT_NAME_REPLACEMENTS)

    # Keep browser/viewport params, but move language to the final suffix for Sphinx.
    for language_id in LANGUAGE_PARAM_IDS:
        filename = filename.replace(f"-{language_id}-", "-")
        filename = filename.replace(f"--{language_id}-", "--")
        filename = filename.removesuffix(f"-{language_id}")

    return Path(screenshots_output_dir, f"{prefix}{filename}{suffix}.png")


def switch_login_language(page, language_menuitem):
    if language_menuitem:
        page.get_by_role("button", name="languages").click()
        page.get_by_role("menuitem", name=language_menuitem).click()


@pytest.mark.screenshots
@pytest.mark.parametrize(
    "screenshot_page", [viewport_size_for_screenshots_1280_720, viewport_size_for_screenshots_1920_1080], indirect=True
)
class TestScreenshotsLogin(object):
    @pytest.mark.parametrize("filename_suffix,login_language", LOGIN_FORM_SCREENSHOTS)
    def test_login_form(self, page, screenshot_page, screenshots_output_dir, request, filename_suffix, login_language):
        login_page = LoginPage(screenshot_page)
        login_page.navigate()
        page = login_page.page
        switch_login_language(page, login_language)
        page.screenshot(path=screenshot_filename(request, screenshots_output_dir, suffix=filename_suffix))

    @pytest.mark.parametrize("filename_suffix,login_language,login_box_text", LOGIN_BOX_SCREENSHOTS)
    def test_login_form_box(
        self,
        screenshot_page,
        screenshots_output_dir,
        request,
        filename_suffix,
        login_language,
        login_box_text,
    ):
        login_page = LoginPage(screenshot_page)
        login_page.navigate()
        page = login_page.page
        switch_login_language(page, login_language)
        login_box = page.get_by_text(login_box_text)
        login_box.screenshot(
            path=screenshot_filename(request, screenshots_output_dir, prefix="box-", suffix=filename_suffix)
        )


@pytest.mark.screenshots
@pytest.mark.parametrize(
    "screenshot_page", [viewport_size_for_screenshots_1280_720, viewport_size_for_screenshots_1920_1080], indirect=True
)
@pytest.mark.parametrize("filename_suffix,target_language", PORTAL_SCREENSHOTS)
class TestScreenshotsPortal(object):
    def test_logged_in(
        self,
        navigate_to_home_page_logged_in_as_admin,
        screenshots_output_dir,
        request,
        screenshot_page,
        filename_suffix,
        target_language,
    ):
        page = navigate_to_home_page_logged_in_as_admin
        switch_language(page, target_language)
        page.screenshot(path=screenshot_filename(request, screenshots_output_dir, suffix=filename_suffix))
