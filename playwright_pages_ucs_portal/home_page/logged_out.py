from playwright_pages_base.base import expect
from .base import HomePage


class HomePageLoggedOut(HomePage):
    """
    This represents the portal homepage from the point-of-view of a user
    who has not yet logged in.
    """

    def set_content(self, *args, **kwargs):
        """
        The saml login tile is often renamed from "Login (Single sign-on)" to "Login"
        This means that login_widget can be plain ucs login or saml login
        while saml_login_tile is always the saml tile, no matter the name.
        """
        super().set_content(*args, **kwargs)
        self.login_widget = self.page.get_by_role("link", name="Login Same tab")
        self.saml_login_tile = self.page.locator('xpath=//a[contains(@href, "univention/saml")]')

    def navigate(self, cookies_accepted=False):
        self.page.goto("/")
        if not cookies_accepted:
            try:
                expect(self.cookie_dialog).to_be_visible()
            except AssertionError:
                pass
            else:
                self.accept_cookies()
        self.logout()
        # Normally, we don't use assertions inside the navigate() methods
        # Navigation roots are the exception, since they have to assure login state
        self.reveal_area(self.right_side_menu, self.header.hamburger_icon)
        expect(self.right_side_menu.login_button).to_be_visible()
        expect(self.right_side_menu.logout_button).to_be_hidden()
        self.hide_area(self.right_side_menu, self.header.hamburger_icon)

    def is_displayed(self):
        expect(self.login_widget).to_be_visible()

    def click_login_widget(self):
        self.login_widget.click()
