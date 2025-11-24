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

from ..portal.conftest import navigate_to_home_page_logged_in_as_admin, browser_context_args

SCREENSHOT_NAME_REPLACEMENTS = str.maketrans(
    {
        "[": "--",
        "]": "",
        "/": "-",
    }
)


@pytest.fixture(scope="session")
def screenshots_output_dir(pytestconfig):
    return pytestconfig.getoption("--screenshots-output-dir")


def screenshot_path(output_dir, name: str, path: str = "") -> Path:
    """
    Assemble the absolut path for the screenshot file.

    :param output_dir: Base directory for the screenshots.
    :param name: Name of the filename without the filename extension. Uses PNG as extension.
    :param path: The path to screenshot inside the base directory. Use it to group screenshots. Defaults to ``""``.
    :return: Absolute path for the screenshot filename.
    """
    return Path(output_dir, path, f"{name}.png")


def screenshot_filename(name: str, suffix: str = "") -> str:
    return f"{name}_{suffix}"


def set_viewport_size(page, width=1920, height=1080):
    page.set_viewport_size({"width": width, "height": height})
    return page


def viewport_size_for_screenshots_1920_1080(page):
    return set_viewport_size(page)


def viewport_size_for_screenshots_1280_720(page):
    return set_viewport_size(page, 1280, 720)


@pytest.fixture
def screenshot_page(request, page):
    page = request.param(page)
    return page
