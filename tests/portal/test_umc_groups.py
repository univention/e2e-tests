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

from e2e.decorators import retrying
from umspages.common.base import expect
from umspages.portal.groups.groups_page import UCSGroupsPage
from umspages.portal.home_page.logged_in import HomePageLoggedIn


@pytest.fixture
def group(udm, faker, wait_for_ldap_secondaries_to_catch_up):
    """
    A group.

    The group will be created for the test case and removed **by** the test case as part of the testing.
    """
    groups_group = udm.get("groups/group")
    test_group = groups_group.new()
    group_name = f"test-{faker.word()}"

    test_group.properties.update(
        {
            "name": group_name,
            "description": faker.sentence(),
        }
    )
    test_group.save()

    wait_for_ldap_secondaries_to_catch_up()
    yield test_group


@pytest.mark.groups
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_create_group_in_umc(
    udm,
    faker,
    navigate_to_home_page_logged_in_as_admin,
    wait_for_ldap_secondaries_to_catch_up,
):
    group_name = faker.user_name()
    group_description = faker.sentence()

    page = navigate_to_home_page_logged_in_as_admin
    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_in.click_groups_tile()
    groups_page = UCSGroupsPage(home_page_logged_in.page)
    groups_page.add_group(group_name, group_description)

    wait_for_ldap_secondaries_to_catch_up()

    ldap_base = udm.get_ldap_base()
    group = udm.get("groups/group").get("cn=%s,cn=groups,%s" % (group_name, ldap_base))
    group.delete()


@pytest.mark.groups
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_edit_group_in_umc(
    group,
    faker,
    navigate_to_home_page_logged_in_as_admin,
    wait_for_ldap_secondaries_to_catch_up,
):
    group_name = group.properties["name"]
    wait_for_ldap_secondaries_to_catch_up()
    previous_group_description = group.properties["description"]
    new_group_description = faker.sentence()

    page = navigate_to_home_page_logged_in_as_admin
    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_in.click_groups_tile()
    groups_page = UCSGroupsPage(home_page_logged_in.page)
    retrying(groups_page.edit_group)(group_name, new_description=new_group_description)

    group.reload()
    assert group.properties["description"] == new_group_description
    assert group.properties["description"] != previous_group_description
    group.delete()


@pytest.mark.groups
@pytest.mark.portal
@pytest.mark.development_environment
@pytest.mark.acceptance_environment
def test_remove_group_in_umc(
    group,
    navigate_to_home_page_logged_in_as_admin,
    wait_for_ldap_secondaries_to_catch_up,
):
    group_name = group.properties["name"]
    wait_for_ldap_secondaries_to_catch_up()

    page = navigate_to_home_page_logged_in_as_admin
    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_in.click_groups_tile()
    groups_page = UCSGroupsPage(home_page_logged_in.page)
    groups_page.remove_group(group_name)
    expect(groups_page.iframe.get_by_role("gridcell", name=group_name)).to_be_hidden()
