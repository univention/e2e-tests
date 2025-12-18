# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import pytest

from univention.admin.rest.client import UDM


@pytest.mark.acceptance_environment
def test_basic_auth(ldap, udm_rest_api):
    udm = UDM.http(udm_rest_api.base_url, ldap.admin_rdn, ldap.admin_password)
    users_module = udm.get("users/user")
    users = users_module.search()
    assert users
    assert len(list(users)) > 0


@pytest.mark.acceptance_environment
def test_oauth_bearer_auth(auth_token, udm_rest_api):
    udm = UDM.bearer(udm_rest_api.base_url, auth_token)
    users_module = udm.get("users/user")
    users = users_module.search()
    assert users
    assert len(list(users)) > 0
