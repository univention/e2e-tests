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


def teardown(main_page):
    main_page.close()


def test_portal_main_page_design(main_page):
    expect(main_page).to_have_title("Sovereign Workplace")

    # There should be 2 portal-category on the page
    categories = main_page.locator('div[class="portal-category"]')
    assert categories.count() == 2

    # The first category should have Login link
    login_widget = (
        categories.locator("nth=0").
        locator('span[class="portal-tile__name"]').
        get_by_text("Login")
    )
    expect(login_widget).to_be_visible()

    # The second category should have LoginSaml link
    login_saml_widget = (
        categories.locator("nth=1").
        locator('span[class="portal-tile__name"]').
        get_by_text("Login")
    )
    expect(login_saml_widget).to_be_visible()

    # Check right side menu is visible
    expect(
        main_page.locator('#header-button-search')
    ).to_be_visible()
    expect(
        main_page.locator('#header-button-bell')
    ).to_be_visible()
    expect(
        main_page.locator('#header-button-menu')
    ).to_be_visible()

    # Check navigation menu
    button_menu = main_page.locator('#header-button-menu')
    button_menu.click()
    menu = main_page.locator("#portal-sidenavigation")
    expect(menu).to_be_visible()
    expect(menu.locator('#loginButton')).to_be_visible()
    expect(menu.locator('a[target="ext_privacystatement"]')).to_be_visible()
    expect(menu.locator('a[target="ext_legalnotice"]')).to_be_visible()


def test_portal_main_page_lang_en(main_page):
    lang = main_page.locator("html").get_attribute("lang")
    assert lang == 'en'

    # Check the page title
    assert main_page.locator('#portal-header').locator('h1', has_text='Sovereign Workplace')

    # Check categories title. There are two categories.
    categories = main_page.locator('div[class="portal-category"]')
    assert categories.count() == 2
    assert categories.locator("nth=0", has_text='Applications')
    assert categories.locator("nth=0", has_text='Sovereign Workplace')

    # Check widgets title. There are two categories.
    assert categories.locator("nth=0", has_text='Login')
    assert categories.locator("nth=0", has_text='Login')

    # Check right side menu text
    button_menu = main_page.locator('#header-button-menu')
    button_menu.click()
    menu = main_page.locator("#portal-sidenavigation")
    assert menu.locator('#loginButton', has_text='LOGIN')
    assert menu.locator('a[target="ext_privacystatement"]', has_text='Privacy statement')
    assert menu.locator('a[target="ext_legalnotice"]', has_text='Legal notice')


def test_portal_main_page_lang_de():
    """
    TODO
    """
    pass


def test_portal_main_page_login_widget(main_page):
    categories = main_page.locator('div[class="portal-category"]')
    assert categories.count() == 2
    login_button = categories.locator("nth=0").locator('a[aria-label="Login Same tab"]', has_text='Login')
    login_button.click()
    main_page.wait_for_load_state("load")
    expect(main_page).to_have_title("Univention Login")


def test_portal_main_page_login_saml_widget(main_page):
    categories = main_page.locator('div[class="portal-category"]')
    assert categories.count() == 2
    login_button = categories.locator("nth=1").locator('a[aria-label="Login Same tab"]', has_text='Login')
    login_button.click()
    main_page.wait_for_load_state("load")
    expect(main_page).to_have_title("Univention Login")


def test_portal_main_page_side_menu_login(main_page):
    button_menu = main_page.locator('#header-button-menu')
    button_menu.click()
    menu = main_page.locator("#portal-sidenavigation")
    login_button = menu.locator('#loginButton')
    login_button.click()
    main_page.wait_for_load_state("load")
    expect(main_page).to_have_title("Univention Login")
