# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2026 Univention GmbH

"""
Fixtures for Keycloak Bootstrap e2e tests.

These tests verify LDAP mapper functionality in Keycloak, particularly
the alwaysReadFromLdap configuration option.
"""

import logging

import pytest

logger = logging.getLogger(__name__)


@pytest.fixture
def ldap_test_user(udm, faker, wait_for_ldap_secondaries_to_catch_up):
    """
    Creates a test user in LDAP with a description attribute.

    The description attribute is used for testing LDAP mapper functionality
    since it's a standard attribute that can be modified.
    """
    users_module = udm.get("users/user")
    user = users_module.new()

    username = f"test-ldapmapper-{faker.user_name()}"
    password = faker.password()
    description = f"initial-description-{faker.uuid4()}"

    user.properties.update(
        {
            "username": username,
            "password": password,
            "firstname": faker.first_name(),
            "lastname": faker.last_name(),
            "description": description,
        }
    )
    user.save()
    wait_for_ldap_secondaries_to_catch_up()

    yield {
        "user": user,
        "username": username,
        "password": password,
        "description": description,
        "dn": user.dn,
    }

    # Cleanup
    try:
        user.reload()
        user.delete()
    except Exception:
        logger.warning("Failed to delete test user %s", username)
