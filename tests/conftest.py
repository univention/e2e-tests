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
import os
import pytest
from urllib.parse import urljoin

from univention.admin.rest.client import UDM


# <https://www.gnu.org/licenses/>.

def pytest_addoption(parser):
    # Portal tests options
    parser.addoption("--portal-base-url", help="Base URL of the univention portal")
    parser.addoption("--username", help="Portal login username")
    parser.addoption("--password", help="Portal login password")
    parser.addoption("--admin-username", help="Portal admin login username")
    parser.addoption("--admin-password", help="Portal admin login password")
    parser.addoption("--udm-admin-username", default="cn=admin", help="UDM admin login password")
    parser.addoption("--udm-admin-password", default="univention", help="UDM admin login password")
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


@pytest.fixture(scope="session")
def udm_admin_username(pytestconfig):
    return pytestconfig.option.udm_admin_username


@pytest.fixture(scope="session")
def udm_admin_password(pytestconfig):
    return pytestconfig.option.udm_admin_password


@pytest.fixture(scope="session")
def portal_base_url(pytestconfig):
    return pytestconfig.getoption("--portal-base-url")


@pytest.fixture()
def udm_rest_api_base_url(portal_base_url):
    """Base URL to reach the UDM Rest API."""
    return urljoin(portal_base_url, "/univention/udm/")


@pytest.fixture
def udm(udm_rest_api_base_url, udm_admin_username, udm_admin_password):
    udm = UDM(udm_rest_api_base_url, udm_admin_username, udm_admin_password)
    # test the connection
    udm.get_ldap_base()
    return udm
