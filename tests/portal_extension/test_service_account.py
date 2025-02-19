# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from contextlib import nullcontext as does_not_raise

from univention.admin.rest.client import UDM


def test_service_account_for_portal_server_exists(udm, ldap_base_dn):
    users_module = udm.get("users/ldap")
    svc_portal_server_dn = f"uid=svc-portal-server,cn=users,{ldap_base_dn}"
    with does_not_raise():
        users_module.get(svc_portal_server_dn)


def test_can_read_users_from_udm_rest_api(udm_rest_api_base_url, portal, ldap_base_dn, k8s):
    udm = UDM(udm_rest_api_base_url, portal.service_account_username, portal.service_account_password)
    users_module = udm.get("users/user")
    administrator_dn = f"uid=Administrator,cn=users,{ldap_base_dn}"
    with does_not_raise():
        users_module.get(administrator_dn)
