# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from contextlib import nullcontext as does_not_raise

import pytest

pytestmark = [
    pytest.mark.development_environment,
    pytest.mark.acceptance_environment,
]


def test_service_account_for_portal_server_exists(udm, portal, ldap_base_dn):
    users_module = udm.get("users/ldap")
    svc_portal_server_dn = f"uid={portal.service_account_username},cn=users,{ldap_base_dn}"
    with does_not_raise():
        users_module.get(svc_portal_server_dn)


def test_can_read_users_from_udm_rest_api(udm_factory, portal, ldap_base_dn, k8s):
    udm = udm_factory(portal.service_account_username, portal.service_account_password)
    users_module = udm.get("users/user")
    administrator_dn = f"uid=Administrator,cn=users,{ldap_base_dn}"
    with does_not_raise():
        users_module.get(administrator_dn)
