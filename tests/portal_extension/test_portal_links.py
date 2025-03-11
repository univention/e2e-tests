# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import pytest

pytestmark = [
    pytest.mark.development_environment,
    pytest.mark.acceptance_environment,
]


def test_portal_supports_link_list(udm, portal_link_list, portal_udm, portal_entry):
    portal_module = udm.get("portals/portal")
    portal_udm.properties[portal_link_list.udm_attr] = [portal_entry.dn]
    portal_udm.save()

    portal_obj = portal_module.get(portal_udm.dn)

    assert portal_obj.properties[portal_link_list.udm_attr] == [portal_entry.dn]


def test_deleted_entry_is_removed_from_link_list(portal_link_list, portal_udm, portal_entry):
    portal_udm.properties[portal_link_list.udm_attr] = [portal_entry.dn]
    portal_udm.save()

    portal_entry.delete()
    portal_udm.reload()

    assert portal_entry.dn not in portal_udm.properties[portal_link_list.udm_attr]
