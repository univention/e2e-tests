# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import pytest

from e2e.api.portal_server import PortalServerApi
from e2e.decorators import retrying_fast
from umspages.portal.home_page.base import HomePage


@pytest.mark.parametrize(
    "portal_link_list",
    [
        "corner_links",
        "menu_links",
        "quick_links",
        "user_links",
    ],
)
def test_result_contains_links(page, portal_link_list):
    home_page = HomePage(page)
    home_page.navigate()
    api = PortalServerApi(page.request)
    result = api.get_portal().json()
    assert portal_link_list in result


def test_added_entry_appears_in_links(page, udm, ldap_base_dn, portal_entry, portal_link_list):
    portal_module = udm.get("portals/portal")
    default_portal = portal_module.get(f"cn=domain,cn=portal,cn=portals,cn=univention,{ldap_base_dn}")
    default_portal.properties[portal_link_list.udm_attr].append(portal_entry.dn)
    default_portal.save()

    home_page = HomePage(page)
    home_page.navigate()
    api = PortalServerApi(page.request)

    @retrying_fast
    def assert_entry_is_in_link_list():
        result = api.get_portal().json()
        assert portal_entry.dn in result[portal_link_list.portal_attr]

    assert_entry_is_in_link_list()
