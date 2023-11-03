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


@pytest.fixture
def browser(playwright):
    browser = playwright.chromium.launch(headless=False)
    browser._close = browser.close

    def _handle_close() -> None:
        browser._close()

    browser.close = _handle_close

    return browser
