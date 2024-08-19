from ...common.base import BasePage


class SetNewPasswordPage(BasePage):
    """
    This is the page one reaches when using the "password reset" functionality.

    This page can only be reached through a second channel like email or sms.
    Either the user or an administrator does request a password reset. This
    will trigger a message to the password recovery email address. The email
    does contain a link with a token which must be used to reach this page.
    """

    def set_content(self, *args, **kwargs):
        super().set_content(*args, **kwargs)
        self.new_password_box = self.page.get_by_role("textbox", name="New password")
        self.retype_password_box = self.page.get_by_test_id("retype-password-box")

        # TODO: Switch to "get_by_role" once the frontend fix is released
        # See: https://git.knut.univention.de/univention/components/univention-portal/-/merge_requests/447

        # self.retype_password_box = self.page.get_by_role("textbox", name="New password (retype)")

        self.submit_button = self.page.get_by_role("button", name="Change password")
        self.password_change_successful_dialog = self.page.get_by_role(
            "dialog", name="Password change successful")

    def navigate(self, url):
        self.page.goto(url)

    def set_new_password(self, password):
        self.new_password_box.fill(password)
        self.retype_password_box.fill(password)
        self.submit_button.click()
