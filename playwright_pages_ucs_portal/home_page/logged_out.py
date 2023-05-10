from playwright_pages_base.base import expect
from .base import HomePage


class HomePageLoggedOut(HomePage):
    """
    This represents the portal homepage from the point-of-view of a user
    who has not yet logged in.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.login_widget = self.page.get_by_role("link", name="Login Same tab")

    def navigate(self):
        self.page.goto("/")
        try:
            expect(self.cookie_dialog).to_be_visible()
        except AssertionError:
            pass
        else:
            self.accept_cookies()
        self.logout()
        # Normally, we don't use assertions inside the navigate() methods
        # Navigation roots are the exception, since they have to assure login state
        self.reveal_right_side_menu()
        expect(self.right_side_menu.login_button).to_be_visible()
        expect(self.right_side_menu.logout_button).to_be_hidden()
        self.hide_right_side_menu()

    def is_displayed(self):
        expect(self.login_widget).to_be_visible()

    def click_login_widget(self):
        self.login_widget.click()
