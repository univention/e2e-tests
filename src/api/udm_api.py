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


class UDMFixtures:
    def __init__(self, base_url, session):
        self._base_url = base_url
        self._session = session

    def ensure_announcement(self, data):
        result_data = self.create_or_update(container="portals/announcement/", data=data)
        return result_data

    def create_or_update(self, container, data):
        container_url = urljoin(self._base_url, container)
        dn = f"cn={data['properties']['name']},{data['position']}"
        resource_url = urljoin(container_url, quote(dn, safe=""))

        if self.resource_exists(resource_url):
            self.create_resource(container_url, data)
        else:
            self.update_resource(resource_url, data)

        verified_data = self.verify_resource(resource_url, data)
        return verified_data

    def resource_exists(self, resource_url):
        result = self._session.get(resource_url)
        # TODO: Non-existing Announcements do lead to a 500 instead of the 404 response.
        # Should check for HTTPStatus.NOT_FOUND instead once fixed.
        return result.status_code != HTTPStatus.OK

    def create_resource(self, container_url, data):
        result = self._session.post(container_url, json=data)
        if result.status_code != HTTPStatus.CREATED:
            raise Exception("Not able to create fixture for test run.")

    def update_resource(self, resource_url, data):
        put_result = self._session.put(resource_url, json=data)
        assert put_result.status_code == HTTPStatus.NO_CONTENT

    def verify_resource(self, resource_url, data):
        result = self._session.get(resource_url)
        result_data = result.json()
        assert result_data["properties"] == data["properties"]
        assert result_data["position"] == data["position"]
        return result_data

    def delete_resource(self, data):
        delete_url = _delete_url_from_resource_data(data)
        response = self._session.delete(delete_url)
        assert response.status_code == HTTPStatus.NO_CONTENT


def _delete_url_from_resource_data(data):
    delete_url = data["_links"]["udm:object/remove"][0]["href"]
    return delete_url
