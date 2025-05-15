# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import pytest
from playwright.sync_api import Locator, Page

from e2e.decorators import retrying_slow
from umspages.common.base import expect
from umspages.portal.home_page.base import HomePage
from umspages.portal.home_page.logged_out import HomePageLoggedOut

from tests.conftest import PortalLinkList


@pytest.fixture(
    params=[
        "navigate_to_home_page_logged_in",
        "navigate_to_home_page_logged_in_as_admin",
        "navigate_to_home_page_logged_out",
    ],
    ids=["home_page_logged_in", "home_page_logged_in_as_admin", "home_page_logged_out"],
)
def portal_page(page: Page, request: pytest.FixtureRequest) -> Page:
    """
    This fixture is parametrized with three different fixtures that represent
    the logged-in as normal user, logged-in as admin and logged out state.
    The corresponding fixture will be dynamically requested using request.getfixturevalue().
    """
    page = request.getfixturevalue(request.param)

    return page


@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_portal_quick_link_folder(
    navigate_to_home_page_logged_out, udm, ldap_base_dn, portal_folder, portal_entry_factory
):
    portal_entries = [portal_entry_factory() for _ in range(3)]
    [portal_folder.properties["entries"].append(portal_entry.dn) for portal_entry in portal_entries]
    portal_folder.save()

    page = navigate_to_home_page_logged_out
    home_page_logged_out = HomePageLoggedOut(page)

    _add_items_into_link_list(udm, ldap_base_dn, PortalLinkList("quickLinks", "quick_links"), [portal_folder.dn])
    portal_folder_name = portal_folder.properties["displayName"]["en_US"]

    loc: Locator = home_page_logged_out.quick_links
    quick_link_button = loc.get_by_role("button", name=portal_folder_name, exact=True)

    assert_locator_visible(page, quick_link_button)
    quick_link_button.click()

    # don't use the retrying assert_locator_visible function here
    # since all the entries should be visible if the button is visible
    for portal_entry in portal_entries:
        portal_entry_name = portal_entry.properties["displayName"]["en_US"]
        expect(loc.get_by_role("link", name=portal_entry_name, exact=True))


@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_portal_links(portal_page: Page, udm, ldap_base_dn, portal_entry_factory, subtests):
    page = HomePage(portal_page)
    for link_list in [PortalLinkList("cornerLinks", "corner_links"), PortalLinkList("quickLinks", "quick_links")]:
        with subtests.test(msg=f"link_list {link_list.portal_attr}"):
            portal_entries = [portal_entry_factory() for _ in range(3)]
            _add_items_into_link_list(
                udm, ldap_base_dn, link_list, [portal_entry.dn for portal_entry in portal_entries]
            )

            for portal_entry in portal_entries:
                portal_entry_name = portal_entry.properties["displayName"]["en_US"]
                link_area: Locator = getattr(page, link_list.portal_attr)
                locator = link_area.get_by_role("link", name=portal_entry_name, exact=True)
                assert_locator_visible(page.page, locator)


@retrying_slow
def assert_locator_visible(page: Page, locator: Locator):
    try:
        expect(locator).to_be_visible(timeout=1000)
    except AssertionError:
        page.reload()
        raise


def _add_items_into_link_list(udm, ldap_base_dn, portal_link_list, items_dn):
    portal_module = udm.get("portals/portal")
    default_portal = portal_module.get(f"cn=domain,cn=portal,cn=portals,cn=univention,{ldap_base_dn}")
    for item_dn in items_dn:
        default_portal.properties[portal_link_list.udm_attr].append(item_dn)
    default_portal.save()
