# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH


def test_group_domain_service_users_exists(udm, ldap_base_dn):
    groups_module = udm.get("groups/group")
    group_dn = f"cn=Domain Service Users,cn=groups,{ldap_base_dn}"
    group = groups_module.get(group_dn)
    assert group
