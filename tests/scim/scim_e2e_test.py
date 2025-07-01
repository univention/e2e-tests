#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

"""
SCIM API End-to-End Test Script

This script tests the SCIM API functionality including:
- User creation and retrieval
- Group creation and retrieval
- Extended attribute mapping for BaWü
"""

import logging
import os
import sys
import uuid

import requests
from requests.auth import HTTPBasicAuth

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", stream=sys.stdout)
logger = logging.getLogger("scim-e2e-test")

# Environment variables (set these in your CI/CD pipeline)
SCIM_BASE_URL = os.getenv("SCIM_BASE_URL", "http://localhost:8080/scim/v2")
SCIM_USERNAME = os.getenv("SCIM_USERNAME", "admin")
SCIM_PASSWORD = os.getenv("SCIM_PASSWORD", "password")
TEST_PREFIX = os.getenv("TEST_PREFIX", "e2e-test-")

# Headers for SCIM requests
HEADERS = {"Content-Type": "application/scim+json", "Accept": "application/scim+json"}

# Authentication
AUTH = HTTPBasicAuth(SCIM_USERNAME, SCIM_PASSWORD)


def create_user():
    """Create a test user with extended attributes"""
    user_id = TEST_PREFIX + str(uuid.uuid4())
    email = f"{user_id}@example.com"

    user_data = {
        "schemas": [
            "urn:ietf:params:scim:schemas:core:2.0:User",
            "urn:ietf:params:scim:schemas:extension:Univention:1.0:User",
            "urn:ietf:params:scim:schemas:extension:UniventionUser:2.0:User",
        ],
        "userName": user_id,
        "name": {"givenName": "Test", "familyName": "User"},
        "emails": [{"value": email, "type": "work", "primary": True}],
        "urn:ietf:params:scim:schemas:extension:Univention:1.0:User": {"passwordRecoveryEmail": email},
        "urn:ietf:params:scim:schemas:extension:UniventionUser:2.0:User": {
            "primaryOrgUnit": "TestOU",
            "secondaryOrgUnits": ["SecondaryOU1", "SecondaryOU2"],
        },
    }

    response = requests.post(f"{SCIM_BASE_URL}/Users", headers=HEADERS, auth=AUTH, json=user_data)

    if response.status_code != 201:
        logger.error(f"User creation failed: {response.status_code} - {response.text}")
        return None

    user = response.json()
    logger.info(f"Created user: {user['id']}")
    return user


def get_user(user_id):
    """Retrieve a user by ID"""
    response = requests.get(f"{SCIM_BASE_URL}/Users/{user_id}", headers=HEADERS, auth=AUTH)

    if response.status_code != 200:
        logger.error(f"User retrieval failed: {response.status_code} - {response.text}")
        return None

    return response.json()


def create_group(user_id=None):
    """Create a test group with extended attributes"""
    group_id = TEST_PREFIX + str(uuid.uuid4())

    group_data = {
        "schemas": [
            "urn:ietf:params:scim:schemas:core:2.0:Group",
            "urn:ietf:params:scim:schemas:extension:Univention:1.0:Group",
        ],
        "displayName": group_id,
        "urn:ietf:params:scim:schemas:extension:Univention:1.0:Group": {"description": "Test Group Description"},
    }

    # Add member if user ID is provided
    if user_id:
        group_data["members"] = [{"value": user_id, "$ref": f"{SCIM_BASE_URL}/Users/{user_id}"}]

    response = requests.post(f"{SCIM_BASE_URL}/Groups", headers=HEADERS, auth=AUTH, json=group_data)

    if response.status_code != 201:
        logger.error(f"Group creation failed: {response.status_code} - {response.text}")
        return None

    group = response.json()
    logger.info(f"Created group: {group['id']}")
    return group


def get_group(group_id):
    """Retrieve a group by ID"""
    response = requests.get(f"{SCIM_BASE_URL}/Groups/{group_id}", headers=HEADERS, auth=AUTH)

    if response.status_code != 200:
        logger.error(f"Group retrieval failed: {response.status_code} - {response.text}")
        return None

    return response.json()


def verify_extended_attributes(user):
    """Verify extended attributes for BaWü"""
    ext1 = user.get("urn:ietf:params:scim:schemas:extension:Univention:1.0:User", {})
    ext2 = user.get("urn:ietf:params:scim:schemas:extension:UniventionUser:2.0:User", {})

    if not ext1.get("passwordRecoveryEmail"):
        raise ValueError("Missing passwordRecoveryEmail in extended attributes")

    if not ext2.get("primaryOrgUnit"):
        raise ValueError("Missing primaryOrgUnit in extended attributes")

    if not ext2.get("secondaryOrgUnits") or len(ext2["secondaryOrgUnits"]) < 1:
        raise ValueError("Missing secondaryOrgUnits in extended attributes")

    logger.info("Extended attributes verified successfully")


def main():
    logger.info("Starting SCIM API E2E tests")
    logger.info(f"Testing endpoint: {SCIM_BASE_URL}")

    # Test user flow
    user = create_user()
    if not user:
        sys.exit(1)

    retrieved_user = get_user(user["id"])
    if not retrieved_user:
        sys.exit(1)

    try:
        verify_extended_attributes(retrieved_user)
    except ValueError as e:
        logger.error(f"Extended attribute verification failed: {str(e)}")
        sys.exit(1)

    # Test group flow
    group = create_group(user["id"])
    if not group:
        sys.exit(1)

    retrieved_group = get_group(group["id"])
    if not retrieved_group:
        sys.exit(1)

    # Verify group attributes
    if "description" not in retrieved_group.get("urn:ietf:params:scim:schemas:extension:Univention:1.0:Group", {}):
        logger.error("Missing description in group extended attributes")
        sys.exit(1)

    logger.info("All SCIM API tests completed successfully")


if __name__ == "__main__":
    main()
