# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from urllib.parse import urljoin

from playwright.sync_api import APIRequestContext

from e2e.decorators import retrying_fast
from e2e.types import LdapDn


class PortalServerApi:
    """
    A model to test the portal server API from the Browser.
    """

    base_path = "/univention/portal/api/v1/"

    def __init__(self, request: APIRequestContext):
        self._request = request

    def get(self, sub_path):
        """
        Retrieve a `sub_path` from the API of the `portal-server`.
        """
        url = urljoin(self.base_path, sub_path)
        response = self._request.get(url)
        return response

    def get_portal(self):
        """
        Utility to help fetch the portal API which has a special path.
        """
        return self.get("../../portal.json")

    @retrying_fast
    def assert_item_is_in_link_list(self, item_dn: LdapDn, link_list: str) -> None:
        """
        Check that an `item_dn` is eventually present in `link_list`.

        The method is retrying to allow for the consumer to update the portal
        cache.
        """
        result = self.get_portal().json()
        assert item_dn in result[link_list]

    @retrying_fast
    def assert_entry(self, entry_dn: LdapDn) -> None:
        """
        Check that an `entry_dn` is present in the portal response.

        The method is retrying to allow for the consumer to update the portal
        cache.
        """
        result = self.get_portal().json()
        included_entries = {entry["dn"] for entry in result["entries"]}
        assert entry_dn in included_entries
