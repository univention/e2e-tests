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

from playwright.sync_api import Page, expect


def test_login(browser, portal_base_url, username, password):
    context = browser.new_context()
    page = context.new_page()
    page.goto(portal_base_url)
    login_widget = page.get_by_text("LoginLog in to the portal")

    expect(login_widget).to_be_visible()

    login_widget.click()
    page.wait_for_load_state("load")

    expect(page).to_have_title("Univention Login")

    username_input = page.locator("#umcLoginUsername")
    password_input = page.locator("#umcLoginPassword")
    login_button = page.get_by_role("button", name="Login")

    expect(username_input).to_be_visible()
    expect(password_input).to_be_visible()
    expect(login_button).to_be_visible()

    username_input.fill(username)
    password_input.fill(password)
    login_button.click()
    page.wait_for_load_state("load")

    expect(page).to_have_title("Sovereign Workplace")

    page.context.storage_state(path="user_page.json")


def test_login_2(page: Page, portal_base_url, username, password):
    page.goto(portal_base_url)
    login_widget = page.get_by_text("LoginLog in to the portal")

    expect(login_widget).to_be_visible()

    login_widget.click()
    page.wait_for_load_state("load")

    expect(page).to_have_title("Univention Login")

    username_input = page.locator("#umcLoginUsername")
    password_input = page.locator("#umcLoginPassword")
    login_button = page.get_by_role("button", name="Login")

    expect(username_input).to_be_visible()
    expect(password_input).to_be_visible()
    expect(login_button).to_be_visible()

    username_input.fill(username)
    password_input.fill(password)
    login_button.click()
    page.wait_for_load_state("load")

    expect(page).to_have_title("Sovereign Workplace")

'''
def test_saml_login(page: Page, portal_base_url, username, password):
    page.goto(portal_base_url)
    # locator('xpath=//a[contains(@href, "univention/saml")]')
    login_widget = page.locator(
        '[href="/univention/saml/?location=%2Funivention%2Fportal%2F"]'
    )

    expect(login_widget).to_be_visible()

    login_widget.click()
    page.wait_for_load_state("load")

    expect(page).to_have_title("Univention Login")

    username_input = page.locator("#umcLoginUsername")
    password_input = page.locator("#umcLoginPassword")
    login_button = page.get_by_role("button", name="Login")

    expect(username_input).to_be_visible()
    expect(password_input).to_be_visible()
    expect(login_button).to_be_visible()

    username_input.fill(username)
    password_input.fill(password)
    login_button.click()
    page.wait_for_load_state("load")

    expect(page).to_have_title("Sovereign Workplace")
'''

def test_logout(browser):
    page = browser.new_page(storage_state="user_page.json")
    page.goto('http://localhost:8000/univention/portal/#/')
    hamburger_icon = page.locator("#header-button-menu")
    right_side_menu = page.locator("#portal-sidenavigation")

    expect(right_side_menu).to_be_hidden()
    hamburger_icon.click()
    expect(right_side_menu).to_be_visible()

    logout_button = page.get_by_role("button", name="Logout")
    expect(logout_button).to_be_visible()
    logout_button.click()
    page.wait_for_load_state("load")

    expect(page).to_have_title("Sovereign Workplace")


def test_logout_2(page: Page, portal_base_url, username, password):
    page.goto(portal_base_url)
    login_widget = page.get_by_text("LoginLog in to the portal")
    login_widget.click()
    page.wait_for_load_state("load")
    page.locator("#umcLoginUsername").fill(username)
    page.locator("#umcLoginPassword").fill(password)
    page.get_by_role("button", name="Login").click()

    hamburger_icon = page.locator("#header-button-menu")
    right_side_menu = page.locator("#portal-sidenavigation")

    expect(right_side_menu).to_be_hidden()
    hamburger_icon.click()
    expect(right_side_menu).to_be_visible()

    logout_button = page.get_by_role("button", name="Logout")
    expect(logout_button).to_be_visible()
    logout_button.click()
    page.wait_for_load_state("load")

    expect(page).to_have_title("Sovereign Workplace")


def test_saml_logout(page: Page, portal_base_url, username, password):
    """
    TODO
    """
    pass
