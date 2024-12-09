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

from umspages.common.base import expect
from umspages.portal.home_page.logged_in import HomePageLoggedIn
from umspages.portal.users.users_page import UCSUsersPage


@pytest.mark.users
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_admin_user_can_view_users_page(navigate_to_home_page_logged_in_as_admin):
    page = navigate_to_home_page_logged_in_as_admin
    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_in.click_users_tile()
    users_page = UCSUsersPage(home_page_logged_in.page)
    # TODO: The user list takes unnaturally long to appear. We are using a locator timeout
    # to handle that. Replace this with an increased global timeout as soon as we figure out how.
    expect(users_page.add_user_button).to_be_visible(timeout=10000)
    expect(users_page.column_header_name).to_be_visible()
    expect(users_page.column_header_path).to_be_visible()
