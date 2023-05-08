from playwright_pages_base.base import BasePage, expect
from playwright_pages_base.portal.common.cookie_dialog import CookieDialog
from playwright_pages_base.portal.common.header import Header
from playwright_pages_base.portal.common.notifications import NotificationDrawer, PopupNotificationContainer
from playwright_pages_base.portal.common.right_side_menu import RightSideMenu
from playwright_pages_base.portal.exceptions import PortalError


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header = Header(self.page.locator("#portal-header"))
        self.notification_drawer = NotificationDrawer(self.page.locator("#notifications-all"))
        self.popup_notification_container = PopupNotificationContainer(
            self.page.locator("#notifications-visible"),
        )
        self.right_side_menu = RightSideMenu(self.page.locator("#portal-sidenavigation"))
        self.cookie_dialog = CookieDialog(self.page.get_by_role("dialog", name="Cookie Consent"))

    def reveal_notification_drawer(self):
        try:
            expect(self.notification_drawer).to_be_hidden()
        except AssertionError:
            pass
        else:
            self.header.click_bell_icon()
            expect(self.notification_drawer).to_be_visible()

    def hide_notification_drawer(self):
        try:
            expect(self.notification_drawer).to_be_visible()
        except AssertionError:
            pass
        else:
            self.header.click_bell_icon()
            expect(self.notification_drawer).to_be_hidden()

    def remove_all_notifications(self):
        self.reveal_notification_drawer()
        count = self.notification_drawer.notifications.count()
        if self.notification_drawer.no_notifications_heading.is_visible():
            if count > 0:
                raise PortalError("'No notifications' visible even when non-zero notifications present")
            else:
                self.hide_notification_drawer()
        elif count == 1:
            self.notification_drawer.notification(0).click_close_button()
            expect(self.notification_drawer).to_be_hidden()
        else:
            self.notification_drawer.click_remove_all_button()
            expect(self.notification_drawer).to_be_hidden()
        self.reveal_notification_drawer()
        expect(self.notification_drawer.no_notifications_heading).to_be_visible()
        expect(self.notification_drawer.notifications).to_have_count(0)
        self.hide_notification_drawer()

    def reveal_right_side_menu(self):
        try:
            expect(self.right_side_menu).to_be_hidden()
        except AssertionError:
            pass
        else:
            self.header.click_hamburger_icon()
            expect(self.right_side_menu).to_be_visible()

    def hide_right_side_menu(self):
        try:
            expect(self.right_side_menu).to_be_visible()
        except AssertionError:
            pass
        else:
            self.header.click_hamburger_icon()
            expect(self.right_side_menu).to_be_hidden()

    def logout(self):
        self.reveal_right_side_menu()
        logout_button_visible = self.right_side_menu.logout_button.is_visible()
        login_button_visible = self.right_side_menu.login_button.is_visible()
        if login_button_visible and logout_button_visible:
            raise PortalError("Both login and logout buttons are visible in the side navigation drawer")
        elif logout_button_visible:
            self.right_side_menu.click_logout_button()

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

        self.reveal_right_side_menu()
        self.right_side_menu.click_entry(change_language_name)
        self.right_side_menu.click_entry(name)
        self.hide_right_side_menu()
