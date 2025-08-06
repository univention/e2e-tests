# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH


import pytest
import requests

from e2e.decorators import retrying_slow


@pytest.mark.central_navigation
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_navigation_api_returns_data_for_anonymous_user(portal):
    response = requests.get(portal.central_navigation_url)
    data = response.json()

    assert response.status_code == requests.codes.ok
    display_name = _get_first_entry(data)["display_name"]
    assert display_name == "Login (Single sign-on)"


@pytest.mark.central_navigation
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_navigation_api_returns_valid_icon_urls(portal):
    response = requests.get(portal.central_navigation_url)
    data = response.json()
    icon_url = _get_first_entry(data)["icon_url"]

    response = requests.get(icon_url)
    assert response.status_code == requests.codes.ok


@pytest.mark.central_navigation
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_navigation_api_returns_data_for_authenticated_user(
    admin_username,
    portal,
):
    response = requests.get(
        portal.central_navigation_url, auth=(admin_username, portal.central_navigation_shared_secret)
    )
    data = response.json()

    assert response.status_code == requests.codes.ok
    # Should not contain the anonymous login
    assert _get_first_entry(data)["display_name"] != "Login (Single sign-on)"
    # Test that the response contains at least some categories
    assert len(data.get("categories", [])) > 0


@pytest.fixture
def restore_default_portal_properties(udm, ldap_base_dn):
    properties_to_backup = ["centralNavigation"]

    portal_module = udm.get("portals/portal")
    portal_obj = portal_module.get(f"cn=domain,cn=portal,cn=portals,cn=univention,{ldap_base_dn}")

    original_properties = {}
    for property in properties_to_backup:
        original_properties[property] = portal_obj.properties[property]

    yield

    portal_obj = portal_module.get(f"cn=domain,cn=portal,cn=portals,cn=univention,{ldap_base_dn}")
    for property in properties_to_backup:
        portal_obj.properties[property] = original_properties[property]

    portal_obj.save()


@pytest.mark.central_navigation
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
@pytest.mark.usefixtures("restore_default_portal_properties")
def test_navigation_api_returns_configured_entries(
    portal,
    admin_username,
    udm,
    ldap_base_dn,
):
    portal_entry_module = udm.get("portals/entry")
    keycloak_entry = portal_entry_module.get(f"cn=keycloak,cn=entry,cn=portals,cn=univention,{ldap_base_dn}")
    custom_navigation = [keycloak_entry.dn]

    portal_module = udm.get("portals/portal")
    portal_obj = portal_module.get(f"cn=domain,cn=portal,cn=portals,cn=univention,{ldap_base_dn}")

    portal_obj.properties["centralNavigation"] = custom_navigation
    portal_obj.save()

    @retrying_slow
    def verify_central_navigation_api_contents():
        response = requests.get(
            portal.central_navigation_url, auth=(admin_username, portal.central_navigation_shared_secret)
        )

        response.raise_for_status()

        data = response.json()

        # Check if the configuration matches expectations
        assert response.status_code == requests.codes.ok
        assert len(data["categories"]) == 1
        assert data["categories"][0]["identifier"] == "domain-admin"
        assert len(data["categories"][0]["entries"]) == 1
        first_entry = data["categories"][0]["entries"][0]
        assert first_entry["identifier"] == "keycloak"

    verify_central_navigation_api_contents()


def _get_first_entry(data):
    first_entry = data["categories"][0]["entries"][0]
    return first_entry
