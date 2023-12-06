from urllib.parse import urljoin

import requests
import pytest


@pytest.fixture
def navigation_api_url(portal_base_url):
    """URL of the navigation API in the Portal."""
    return urljoin(portal_base_url, "/univention/portal/navigation.json")


def test_navigation_api_returns_data_for_anonymous_user(navigation_api_url):
    response = requests.get(navigation_api_url)
    data = response.json()

    assert response.status_code == requests.codes.ok
    assert data["categories"][0]["entries"][0]["display_name"] == "Login"


def test_navigation_api_returns_valid_icon_urls(navigation_api_url):
    response = requests.get(navigation_api_url)
    data = response.json()
    icon_url = data["categories"][0]["entries"][0]["icon_url"]

    response = requests.get(icon_url)
    assert response.status_code == requests.codes.ok
