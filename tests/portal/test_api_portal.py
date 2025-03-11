# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import time
from urllib.parse import urljoin

import pytest
import requests

from e2e.api.portal_server import PortalServerApi
from univention.admin.rest.client import UDM


def test_result_contains_links(page, portal_link_list):
    api = PortalServerApi(page.request)
    result = api.get_portal().json()
    assert portal_link_list.portal_attr in result


def test_added_entry_appears_in_links(page, udm, ldap_base_dn, portal_entry, portal_link_list):
    _add_item_into_link_list(udm, ldap_base_dn, portal_link_list, portal_entry.dn)
    api = PortalServerApi(page.request)
    api.assert_item_is_in_link_list(portal_entry.dn, portal_link_list.portal_attr)


def test_added_folder_appears_in_links(
    page,
    udm,
    ldap_base_dn,
    portal_entry,
    portal_folder,
    portal_link_list,
):
    portal_folder.properties["entries"].append(portal_entry.dn)
    portal_folder.save()
    _add_item_into_link_list(udm, ldap_base_dn, portal_link_list, portal_folder.dn)
    api = PortalServerApi(page.request)
    api.assert_item_is_in_link_list(portal_folder.dn, portal_link_list.portal_attr)


def _add_item_into_link_list(udm, ldap_base_dn, portal_link_list, item_dn):
    portal_module = udm.get("portals/portal")
    default_portal = portal_module.get(f"cn=domain,cn=portal,cn=portals,cn=univention,{ldap_base_dn}")
    default_portal.properties[portal_link_list.udm_attr].append(item_dn)
    default_portal.save()


@pytest.fixture
def portal_entry(udm, ldap_base_dn, portal_entry):
    """Portal Entry in a Portal Category."""
    # Add portal_entry to the portal categories to make it visible and accessible through the URL
    # f"{portal_endpoint}/univention/portal/portal.json"
    category = udm.obj_by_dn(f"cn=domain-service,cn=category,cn=portals,cn=univention,{ldap_base_dn}")
    category.properties["entries"].append(portal_entry.dn)
    category.save()
    return portal_entry


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
def test_create_portal_entry(portal_entry, wait_for_portal_update):
    entry_exists = wait_for_portal_update(portal_entry.dn)
    assert entry_exists
