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

import time
import uuid
from contextlib import contextmanager
from urllib.parse import urljoin

import pytest
import requests

from univention.admin.rest.client import UDM


@contextmanager
def create_visible_portal_entry(udm: UDM, ldap_base_dn):
    portals = udm.get("portals/entry")
    assert portals
    portal_entry = portals.new()
    portal_entry.properties.update({
        "name": str(uuid.uuid1()),
        "description": {"en_US": "New portal tile"},
        "displayName": {"en_US": "New portal tile"},
        "link": [["en_US", "http://example.com"]],
        "activated": True,

    })
    portal_entry.save()

    # Add portal_entry to the portal categories to make it visible and accessible through the URL
    # f"{portal_endpoint}/univention/portal/portal.json"
    category = udm.obj_by_dn(f"cn=domain-service,cn=category,cn=portals,cn=univention,{ldap_base_dn}")
    category.properties["entries"].append(portal_entry.dn)
    category.save()

    try:
        yield portal_entry
    finally:
        portal_entry.delete()


@pytest.fixture
def portal_api_url(portal_base_url):
    """URL of the portal API in the Portal."""
    return urljoin(portal_base_url, "/univention/portal/portal.json")


@pytest.fixture()
def wait_for_portal_update(udm: UDM, portal_base_url: str, portal_api_url):
    def _wait_for_entry(entry_dn: str, timeout=30.0) -> bool:
        start_time = time.time()
        while time.time() - start_time < timeout:
            response = requests.get(portal_api_url)
            assert response.status_code == 200

            entries = response.json()["entries"]
            if any(entry.get("dn") == entry_dn for entry in entries):
                return True
            time.sleep(0.1)
        return False

    return _wait_for_entry


@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_create_portal_entry(udm, wait_for_portal_update, ldap_base_dn):
    with create_visible_portal_entry(udm, ldap_base_dn) as portal_entry:
        entry_exists = wait_for_portal_update(portal_entry.dn)
        assert entry_exists
