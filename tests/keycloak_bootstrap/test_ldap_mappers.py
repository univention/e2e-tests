# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2026 Univention GmbH

"""
Tests for Keycloak Bootstrap LDAP Mapper functionality.

These tests verify that the LDAP mapper configuration works correctly,
particularly the `alwaysReadFromLdap` option which ensures mutable
LDAP attributes are always read fresh from LDAP instead of Keycloak's cache.

Requires CI values configuration:
    nubusKeycloakBootstrap:
      bootstrap:
        ldapMappers:
          description:
            alwaysReadFromLdap: true
"""

import logging
import time

import pytest

logger = logging.getLogger(__name__)

pytestmark = [
    pytest.mark.development_environment,
    pytest.mark.acceptance_environment,
]


class TestLdapMapperAlwaysReadFromLdap:
    """
    Tests for the alwaysReadFromLdap LDAP mapper configuration.

    When alwaysReadFromLdap is enabled, Keycloak should always fetch the
    attribute value from LDAP instead of using its cached/imported value.
    """

    def test_user_attribute_is_synced_from_ldap(
        self,
        ldap_test_user,
        keycloak_admin,
    ):
        """
        Verify that user attributes configured with LDAP mappers are available in Keycloak.
        """
        username = ldap_test_user["username"]
        time.sleep(2)

        users = keycloak_admin.get_users({"username": username})
        assert len(users) == 1, f"Expected 1 user with username {username}, found {len(users)}"

        kc_user = users[0]
        assert kc_user["username"] == username
        assert kc_user.get("attributes", {}).get("displayName", [None])[0] is not None

    def test_ldap_attribute_change_reflected_in_keycloak(
        self,
        ldap_test_user,
        keycloak_admin,
        wait_for_ldap_secondaries_to_catch_up,
    ):
        """
        Verify that changes to LDAP attributes with alwaysReadFromLdap are reflected in Keycloak.

        Modifying the 'description' attribute in LDAP should be visible in Keycloak
        immediately since it's configured with alwaysReadFromLdap: true.
        """
        username = ldap_test_user["username"]
        user_obj = ldap_test_user["user"]
        initial_description = ldap_test_user["description"]
        time.sleep(2)

        users = keycloak_admin.get_users({"username": username})
        assert len(users) == 1
        kc_user_id = users[0]["id"]

        # Verify initial description is synced
        kc_user = keycloak_admin.get_user(kc_user_id)
        description_in_kc = kc_user.get("attributes", {}).get("description", [None])[0]
        assert description_in_kc == initial_description

        # Modify description in LDAP
        new_description = f"updated-description-{time.time()}"
        user_obj.reload()
        user_obj.properties["description"] = new_description
        user_obj.save()
        wait_for_ldap_secondaries_to_catch_up()

        time.sleep(2)

        # Verify updated description is reflected in Keycloak
        kc_user = keycloak_admin.get_user(kc_user_id)
        description_in_kc = kc_user.get("attributes", {}).get("description", [None])[0]

        assert description_in_kc == new_description, (
            f"Expected Keycloak to have updated description '{new_description}', "
            f"but found '{description_in_kc}'. "
            "Ensure ldapMappers.description is configured with alwaysReadFromLdap: true."
        )
