from urllib.parse import urljoin

import pytest
import requests


@pytest.fixture
def navigation_api_url(portal_base_url):
    """URL of the navigation API in the Portal."""
    return urljoin(portal_base_url, "/univention/portal/navigation.json")


@pytest.mark.central_navigation
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_navigation_api_returns_data_for_anonymous_user(navigation_api_url):
    response = requests.get(navigation_api_url)
    data = response.json()

    assert response.status_code == requests.codes.ok
    display_name = _get_first_entry(data)["display_name"]
    assert display_name == "Login"


@pytest.mark.central_navigation
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_navigation_api_returns_valid_icon_urls(navigation_api_url):
    response = requests.get(navigation_api_url)
    data = response.json()
    icon_url = _get_first_entry(data)["icon_url"]

    response = requests.get(icon_url)
    assert response.status_code == requests.codes.ok


def _get_first_entry(data):
    first_entry = data["categories"][0]["entries"][0]
    return first_entry
