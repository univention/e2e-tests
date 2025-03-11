# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from e2e.api.portal_server import PortalServerApi


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
