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

from playwright.sync_api import expect

from umspages.portal.main_page import MainPage


def test_portal_main_page_design(
        main_page: MainPage
):
    page = main_page

    assert page.title == 'Sovereign Workplace'

    expect(page.category_1).to_be_visible()
    expect(page.category_2).to_be_visible()
    expect(page.login_widget).to_be_visible()
    expect(page.login_saml_widget).to_be_visible()
    expect(page.search).to_be_visible()
    expect(page.bell).to_be_visible()
    expect(page.menu).to_be_visible()

    # Check navigation menu
    expect(page.menu_login_button).not_to_be_visible()
    expect(page.menu_privacy_button).not_to_be_visible()
    expect(page.menu_legalnotice_button).not_to_be_visible()

    page.menu.click()

    expect(page.menu_login_button).to_be_visible()
    expect(page.menu_privacy_button).to_be_visible()
    expect(page.menu_legalnotice_button).to_be_visible()


def test_portal_main_page_lang_en(
        main_page: MainPage
):
    page = main_page
    assert page.lang == 'en'

    # Check the page title
    assert page.header == 'Sovereign Workplace'

    # Check categories title. There are two categories.
    assert page.category_1.locator("h2").inner_text() == 'Applications'
    assert page.category_2.locator("h2").inner_text() == 'Sovereign Workplace'

    # Check widgets title. There are two categories.
    assert page.category_1.locator(".portal-tile__name").inner_text() == 'Login'
    assert page.category_2.locator(".portal-tile__name").inner_text() == 'Login'

    page.menu.click()

    # Check right side menu text
    assert page.menu_login_button.inner_text() == 'LOGIN'
    assert page.menu_privacy_button.inner_text() == 'Privacy statement'
    assert page.menu_legalnotice_button.inner_text() == 'Legal notice'


def test_portal_main_page_lang_de(
        main_page: MainPage
):
    """
    TODO
    """
    # assert 'de' == main_page.locator("html").get_attribute("lang")
    pass


def test_portal_main_page_login_widget(
        main_page: MainPage
):
    pass


def test_portal_main_page_login_saml_widget(
        main_page: MainPage
):
    pass


def test_portal_main_page_side_menu_login(
        main_page: MainPage
):
    pass
