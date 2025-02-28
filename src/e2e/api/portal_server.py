# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from urllib.parse import urljoin

from playwright.sync_api import APIRequestContext


class PortalServerApi:
    """
    A model to test the portal server API.
    """

    base_path = "/univention/portal/api/v1/"

    def __init__(self, request: APIRequestContext):
        self._request = request

    def get(self, sub_path):
        url = urljoin(self.base_path, sub_path)
        response = self._request.get(url)
        return response
