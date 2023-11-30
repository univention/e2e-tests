# Like what you see? Join us!
# https://www.univention.com/about-us/careers/vacancies/
#
# Copyright 2001-2023 Univention GmbH
#
# https://www.univention.de/
#
# All rights reserved.
#
# The source code of this program is made available
# under the terms of the GNU Affero General Public License version 3
# (GNU AGPL V3) as published by the Free Software Foundation.
#
# Binary versions of this program provided by Univention to you as
# well as other copyrighted, protected or trademarked materials like
# Logos, graphics, fonts, specific documentations and configurations,
# cryptographic keys etc. are subject to a license agreement between
# you and Univention and not subject to the GNU AGPL V3.
#
# In the case you use this program under the terms of the GNU AGPL V3,
# the program is provided in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License with the Debian GNU/Linux or Univention distribution in file
# /usr/share/common-licenses/AGPL-3; if not, see
# <https://www.gnu.org/licenses/>.

from http import HTTPStatus
from urllib.parse import quote, urljoin

import requests


class UDMSession:
    """
    Prepares an instance of `requests.Session` to call the UDM Rest API.

    The instance has headers and authentication information prepared so that
    requests will run with full permissions in the UDM Rest API.
    """

    def __init__(
            self,
            base_url,
            udm_admin_username,
            udm_admin_password,
    ):
        self._base_url = base_url
        self._session = requests.Session()
        self._session.auth = (udm_admin_username, udm_admin_password)
        self._session.headers.update({"accept": "application/json"})
        self._base_announcement_url = urljoin(
            self._base_url,
            "portals/announcement/"
        )

    def get_announcement_url(self, announcement: dict) -> str:
        dn = f"cn={announcement['properties']['name']}, {announcement['position']}"
        return urljoin(
            self._base_announcement_url, quote(dn, safe="")
        )

    def check_announcement_exists(self, announcement: dict):
        result = self._session.get(
            self.get_announcement_url(announcement)
        )
        return result.status_code == HTTPStatus.OK

    def create_announcement(self, announcement: dict):
        result = self._session.post(
            self._base_announcement_url,
            json=announcement
        )
        if result.status_code != HTTPStatus.CREATED:
            raise Exception('Cannot create test announcement. '
                            'Error code {}'.format(result.status_code))

    def remove_announcement(self, announcement: dict):
        result = self._session.delete(
            self.get_announcement_url(announcement)
        )
        if result.status_code != HTTPStatus.NO_CONTENT:
            raise Exception('Cannot delete test announcement. '
                            'Error code {}'.format(result.status_code))
