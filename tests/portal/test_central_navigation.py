# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import pytest
import requests


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


def _get_first_entry(data):
    first_entry = data["categories"][0]["entries"][0]
    return first_entry
