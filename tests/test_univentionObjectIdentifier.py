# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import uuid

import pytest
import requests
from requests.auth import HTTPBasicAuth


@pytest.fixture
def create_object_identifier_user(udm, faker, email_domain):
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

    def _create(extra_properties: dict | None = None):
        test_user.properties.update(extra_properties or {})
        test_user.save()
        return test_user

    yield _create

    test_user.reload()
    test_user.delete()


@pytest.fixture
def create_object_identifier_group(udm, faker):
    groups_group = udm.get("groups/group")
    test_group = groups_group.new()
    group_name = f"test-{faker.word()}"

    test_group.properties.update(
        {
            "name": group_name,
            "description": faker.sentence(),
        }
    )

    def _create(extra_properties: dict | None = None):
        test_group.properties.update(extra_properties or {})
        test_group.save()
        return test_group

    yield _create

    test_group.reload()
    test_group.delete()


@pytest.fixture
def create_object_identifier_portal_obj(udm, faker):
    portal_module = udm.get("portals/portal")
    portal_obj = portal_module.new()
    portal_name = f"test-{faker.slug()}"
    portal_obj.properties.update(
        {
            "name": portal_name,
            "displayName": {
                "en_US": faker.catch_phrase(),
            },
        }
    )

    def _create(extra_properties: dict | None = None):
        portal_obj.properties.update(extra_properties or {})
        portal_obj.save()
        return portal_obj

    yield _create

    portal_obj.reload()
    portal_obj.delete()


@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_user_autogenerated_univentionObjectIdentifier(create_object_identifier_user):
    user = create_object_identifier_user()
    assert user
    user.reload()
    assert user.properties["univentionObjectIdentifier"]


@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_user_explicitly_set_univentionObjectIdentifier(create_object_identifier_user):
    test_identifier = str(uuid.uuid4())
    user = create_object_identifier_user(
        {
            "univentionObjectIdentifier": test_identifier,
        }
    )
    assert user
    user.reload()
    assert user.properties["univentionObjectIdentifier"] == test_identifier


@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_group_autogenerated_univentionObjectIdentifier(create_object_identifier_group):
    group = create_object_identifier_group()
    assert group
    group.reload()
    assert group.properties["univentionObjectIdentifier"]


@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_group_explicitly_set_univentionObjectIdentifier(create_object_identifier_group):
    test_identifier = str(uuid.uuid4())
    group = create_object_identifier_group(
        {
            "univentionObjectIdentifier": test_identifier,
        }
    )
    assert group
    group.reload()
    assert group.properties["univentionObjectIdentifier"] == test_identifier


@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_portal_obj_autogenerated_univentionObjectIdentifier(create_object_identifier_portal_obj):
    """
    Randomly chosen UDM module to validate that univentionObjectIdentifier is not only configurable on Users and Groups objects
    """
    portal_obj = create_object_identifier_portal_obj()
    assert portal_obj
    portal_obj.reload()
    assert portal_obj.properties["univentionObjectIdentifier"]


@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_portal_obj_explicitly_set_univentionObjectIdentifier(create_object_identifier_portal_obj):
    """
    Randomly chosen UDM module to validate that univentionObjectIdentifier is not only configurable on Users and Groups objects
    """
    test_identifier = str(uuid.uuid4())
    portal_obj = create_object_identifier_portal_obj(
        {
            "univentionObjectIdentifier": test_identifier,
        }
    )
    assert portal_obj
    portal_obj.reload()
    assert portal_obj.properties["univentionObjectIdentifier"] == test_identifier


@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_openapi_schema(udm_rest_api, ldap, subtests):
    response = requests.get(
        f"{udm_rest_api.base_url}openapi.json",
        headers={"Accept": "application/json"},
        auth=HTTPBasicAuth(ldap.admin_rdn, ldap.admin_password),
    )
    response.raise_for_status()
    openapi_schema = response.json()
    assert openapi_schema

    blocklist_exceptions = [
        f"blocklists-{suffix}" for suffix in ["list.request", "list.request-patch", "entry.request-patch"]
    ]

    for component, schema in openapi_schema["components"]["schemas"].items():
        props = schema.get("properties", {}).get("properties", {}).get("properties", {})
        if component in blocklist_exceptions:
            continue
        with subtests.test(msg=component, i=component):
            if component.endswith("request-patch") and component != "users-passwd.request-patch":
                assert "univentionObjectIdentifier" in props.keys()
            else:
                assert "univentionObjectIdentifier" not in props.keys()


@pytest.mark.development_environment
@pytest.mark.acceptance_environment
@pytest.mark.parametrize("group_name", ("Domain Users", "Domain Admins"))
def test_object_has_univentionObjectIdentifier(udm, group_name):
    groups_group = udm.get("groups/group")
    group = groups_group.get(f"cn={group_name},cn=groups,{udm.get_ldap_base()}")

    assert "univentionObjectIdentifier" in group.properties
    assert uuid.UUID(group.properties["univentionObjectIdentifier"])
