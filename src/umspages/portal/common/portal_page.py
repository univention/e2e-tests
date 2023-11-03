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

from ...common.base import (BasePage,  # type: ignore
                            expect)  # type: ignore
from ..exceptions import PortalError
from .cookie_dialog import CookieDialog
from .header import Header
from .notifications import NotificationDrawer, PopupNotificationContainer
from .right_side_menu import RightSideMenu


class PortalPage(BasePage):
    """
    All portal pages should be derived from this class.
    Access to shared parts (i.e. parts that all pages have) are provided using
    instance variables. For example, to get the header, you can do
    the following.

    ```
    class MyPage(PortalPage):
        ...

    def test_something(page):
        my_page = MyPage(page)
        header = my_page.header  # Get the navigation header
        # Now, do something with the header
        header.reveal_notification_drawer()
    ```
    """

    def set_content(self, *args, **kwargs):
        super().set_content(*args, **kwargs)
        self.header = Header(self.page.locator("#portal-header"))
        self.notification_drawer = NotificationDrawer(
            self.page.locator("#notifications-all")
        )
        self.popup_notification_container = PopupNotificationContainer(
            self.page.locator("#notifications-visible"),
        )
        self.right_side_menu = RightSideMenu(
            self.page.locator("#portal-sidenavigation")
        )
        self.cookie_dialog = CookieDialog(
            self.page.get_by_role("dialog", name="Cookie Consent")
        )

    def remove_all_notifications(self):
        self.reveal_area(self.notification_drawer, self.header.bell_icon)
        count = self.notification_drawer.notifications.count()
        if self.notification_drawer.no_notifications_heading.is_visible():
            if count > 0:
                raise PortalError(
                    "'No notifications' visible even when non-zero"
                    " notifications present"
                )
            else:
                self.hide_area(self.notification_drawer, self.header.bell_icon)
        elif count == 1:
            self.notification_drawer.notification(0).click_close_button()
            expect(self.notification_drawer).to_be_hidden()
        else:
            self.notification_drawer.click_remove_all_button()
            expect(self.notification_drawer).to_be_hidden()
        self.reveal_area(self.notification_drawer, self.header.bell_icon)
        expect(
            self.notification_drawer.no_notifications_heading
        ).to_be_visible()
        expect(self.notification_drawer.notifications).to_have_count(0)
        self.hide_area(self.notification_drawer, self.header.bell_icon)

    def logout(self):
        """Optimized for the case when we are already logged out"""
        self.reveal_area(self.right_side_menu, self.header.hamburger_icon)
        try:
            expect(self.right_side_menu.login_button).to_be_visible()
        except AssertionError:
            try:
                expect(self.right_side_menu.logout_button).to_be_visible()
            except AssertionError:
                raise PortalError(
                    "Both login and logout buttons are "
                    "hidden in the side navigation drawer"
                )
            self.right_side_menu.click_logout_button()
        else:
            try:
                expect(self.right_side_menu.logout_button).to_be_hidden()
            except AssertionError:
                raise PortalError(
                    "Both login and logout buttons are visible "
                    "in the side navigation drawer"
                )
            self.hide_area(self.right_side_menu, self.header.hamburger_icon)

    def accept_cookies(self):
        expect(self.cookie_dialog).to_be_visible()
        self.cookie_dialog.click_accept_button()
        expect(self.cookie_dialog).to_be_hidden()

    def get_language(self):
        html_tag = self.page.locator("html")
        return html_tag.get_attribute("lang")

    def switch_language(self, name):
        menu_entry_names = {
            "en": "Change Language",
            "de": "Sprache ändern",
        }
        # TODO: Always should set the "lang" attribute.
        # See https://git.knut.univention.de/univention/components/univention-portal/-/issues/708
        current_language = self.get_language() or "en"
        change_language_name = menu_entry_names[current_language]

        self.reveal_area(self.right_side_menu, self.header.hamburger_icon)
        self.right_side_menu.click_entry(change_language_name)
        self.right_side_menu.click_entry(name)
        self.hide_area(self.right_side_menu, self.header.hamburger_icon)

    def assert_logged_in(self):
        self.reveal_area(self.right_side_menu, self.header.hamburger_icon)
        # Checking login state only since is_displayed() is currently empty
        expect(self.right_side_menu.logout_button).to_be_visible()
        expect(self.right_side_menu.login_button).to_be_hidden()
        self.hide_area(self.right_side_menu, self.header.hamburger_icon)

    def assert_logged_out(self):
        self.reveal_area(self.right_side_menu, self.header.hamburger_icon)
        expect(self.right_side_menu.login_button).to_be_visible()
        expect(self.right_side_menu.logout_button).to_be_hidden()
        self.hide_area(self.right_side_menu, self.header.hamburger_icon)
