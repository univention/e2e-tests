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

import pytest

from umspages.portal.login_page import LoginPage


@pytest.mark.gaia
@pytest.mark.devenv
class TestCookies:
    def _get_cookie(self, cookies, name):
        return [c for c in cookies if c["name"] == name]

    def test_cookie_hardening_sets_samesite(
            self,
            login_page: LoginPage,
            username,
            password,
    ):
        login_page.login(username, password)
        session_cookie = self._get_cookie(
            login_page._page.context.cookies(),
            "UMCSessionId"
        )

        assert session_cookie

        checks = [
            session_cookie[0].get('sameSite', None),
            session_cookie[0].get('secure', None),
            session_cookie[0].get('expires', None),
        ]

        assert checks == ['Strict', True, -1]
