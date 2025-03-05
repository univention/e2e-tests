# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH


import pytest


@pytest.fixture
def portal_udm(udm, faker, ldap_base_dn):
    """
    Creates a Portal object via UDM Rest API.

    The object is as minimal as possible and will be cleaned up after the test
    run.
    """
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
    portal_obj.save()

    yield portal_obj

    portal_obj.reload()
    portal_obj.delete()


@pytest.fixture
def portal_entry(udm, faker, ldap_base_dn):
    """
    Creates an activated test Portal Entry.

    The Portal Entry will be isolated, it will not be added into any Portal or
    Category.

    The entry will be cleaned up after the test run.
    """
    entry_module = udm.get("portals/entry")
    portal_entry = entry_module.new()
    portal_entry.properties.update(
        {
            "name": faker.slug(),
            "description": {"en_US": faker.catch_phrase()},
            "displayName": {"en_US": faker.catch_phrase()},
            "link": [["en_US", "http://test.example.com"]],
            "activated": True,
        }
    )
    portal_entry.save()

    yield portal_entry

    portal_entry.reload()
    portal_entry.delete()


pytestmark = pytest.mark.parametrize(
    "portal_link_list",
    [
        "cornerLinks",
        "menuLinks",
        "quickLinks",
        "userLinks",
    ],
)


def test_portal_supports_link_list(udm, portal_link_list, portal_udm, portal_entry):
    portal_module = udm.get("portals/portal")
    portal_udm.properties[portal_link_list] = [portal_entry.dn]
    portal_udm.save()

    portal_obj = portal_module.get(portal_udm.dn)

    assert portal_obj.properties[portal_link_list] == [portal_entry.dn]
