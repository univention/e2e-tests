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

from lang import de, en

def pytest_addoption(parser):

    # Testing options
    parser.addoption("--browser_name",
                     type=str,
                     default='chromium',
                     help="Web browser name: "
                          "chromium, firefox, webkit",
                     )
    '''parser.addoption("--headed",
                     action="store_false",
                     help="Run tests in headed mode. See more:"
                          "https://playwright.dev/python/docs/ci#running-headed",
                     )'''
    parser.addoption("--slow-mo",
                     action="store",
                     type=int,
                     default=0,
                     help="Integer value."
                          "Slows down Playwright operations by the specified "
                          "amount of milliseconds. Useful so that you can see "
                          "what is going on (default: 0).  See more: "
                          "https://playwright.dev/python/docs/test-runners#configure-slow-mo",
                     )
    parser.addoption("--is-mobile",
                     action="store",
                     default=False,
                     help="False (default) or True."
                          "Select desktop or mobile version of the site.",
                     )
    parser.addoption("--time-zone",
                     action="store",
                     default='Europe/Berlin',
                     help="",
                     )
    parser.addoption("--locale",
                     action="store",
                     default='en-EN',
                     help="String: 'en-EN' or 'de-DE'",
                     )

    # Portal tests options
    parser.addoption("--portal-base-url", help="Base URL of the univention portal")
    parser.addoption("--username", help="Portal login username")
    parser.addoption("--password", help="Portal login password")
    parser.addoption("--admin-username", help="Portal admin login username")
    parser.addoption("--admin-password", help="Portal admin login password")
    # BFP tests options
    parser.addoption("--keycloak-base-url", help="Base URL of Keycloak")
    parser.addoption("--kc-admin-username", default="admin",
                     help="Keycloak admin login username"
                     )
    parser.addoption("--kc-admin-password", default="univention",
                     help="Keycloak admin login password"
                     )
    parser.addoption("--num-device-block", type=int, default=5,
                     help="Number of failed logins for device block"
                     )
    parser.addoption("--num-ip-block", type=int, default=7,
                     help="Number of failed logins for IP block"
                     )
    parser.addoption("--release-duration", type=int, default=60,
                     help="Blocks are released after this many seconds"
                     )
    parser.addoption("--realm", default="master",
                     help="Realm to attempt logins at"
                     )


@pytest.fixture(scope="module")
def localization(pytestconfig) -> dict:
    if 'de-DE' == pytestconfig.getoption("--locale"):
        return de.handbook
    return en.handbook


# It should be in the end of the file
pytest_plugins = [
    "fixtures.bfp",
    "fixtures.portal",
  ]
