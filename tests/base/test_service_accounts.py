# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from contextlib import nullcontext as does_not_raise
from typing import NamedTuple

import pytest

from univention.admin.rest.client import UDM


@pytest.fixture
def domain_service_users_dn(ldap_base_dn):
    """
    DN of the group "Domain Service Users".
    """
    group_dn = f"cn=Domain Service Users,cn=groups,{ldap_base_dn}"
    return group_dn


class UserAndPassword(NamedTuple):
    user: object
    password: str


@pytest.fixture
def domain_service_user(udm, faker, domain_service_users_dn) -> UserAndPassword:
    """
    A service account user.
    """
    users_user = udm.get("users/ldap")
    user = users_user.new()
    username = f"test-svc-{faker.user_name()}"
    password = faker.password()
    user.properties.update(
        {
            "username": username,
            "password": password,
        }
    )
    user.save()

    groups_module = udm.get("groups/group")
    domain_service_users = groups_module.get(domain_service_users_dn)
    domain_service_users.properties["users"].append(user.dn)
    domain_service_users.save()

    return UserAndPassword(user, password)


def test_group_domain_service_users_exists(udm, domain_service_users_dn):
    groups_module = udm.get("groups/group")
    with does_not_raise():
        groups_module.get(domain_service_users_dn)


def test_domain_service_user_accesses_udm_rest_api(
    udm_rest_api_base_url,
    domain_service_user: UserAndPassword,
):
    username = domain_service_user.user.properties["username"]
    udm = UDM(udm_rest_api_base_url, username, domain_service_user.password)
    with does_not_raise():
        udm.get_ldap_base()
