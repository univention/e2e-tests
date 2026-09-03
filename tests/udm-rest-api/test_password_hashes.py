# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

"""
Password hashes on a user object written by the UDM REST API.

Checks a newly created account, and the same account after a password change:
the Kerberos enctypes, the `userPassword` scheme, the absence of a
`sambaNTPassword`, the key version number, and that a password change replaces
all key material.
"""

import pytest

from e2e.password_hashes import assert_password_hashes, read_password_hashes

pytestmark = [
    pytest.mark.password_hashes,
    pytest.mark.development_environment,
    pytest.mark.acceptance_environment,
]


@pytest.fixture
def user(udm, faker, email_domain):
    """
    A user created through the UDM REST API, with a password.
    """
    users_user = udm.get("users/user")
    test_user = users_user.new()
    username = f"test-{faker.user_name()}"
    test_user.properties.update(
        {
            "firstname": faker.first_name(),
            "lastname": faker.last_name(),
            "username": username,
            "displayName": faker.name(),
            "password": faker.password(),
            "mailPrimaryAddress": f"{username}@{email_domain}",
        }
    )
    test_user.save()

    yield test_user

    test_user.reload()
    test_user.delete()


def test_password_hashes_of_a_user(user, faker, ldap_primary, subtests):
    """
    A new account carries the expected hashes, and a password change keeps them.
    """
    created = read_password_hashes(ldap_primary, user.dn)

    with subtests.test("new account"):
        assert_password_hashes(created, user.dn, key_version_number=1)

    user.properties["password"] = faker.password()
    user.save()
    changed = read_password_hashes(ldap_primary, user.dn)

    with subtests.test("after a password change"):
        assert_password_hashes(changed, user.dn, key_version_number=2)

    with subtests.test("the key material is rotated"):
        assert set(changed["krb5key"]).isdisjoint(created["krb5key"]), (
            f"{user.dn} kept Kerberos key material across a password change"
        )
        assert changed["userpassword"] != created["userpassword"]
