from ..common.portal_page import PortalPage


class PasswordForgottenPage(PortalPage):

    def set_content(self, *args, **kwargs):
        super().set_content(*args, **kwargs)
        self.password_forgotten_dialog = self.page.get_by_role("dialog", name="Password forgotten")
        self.username_input = self.password_forgotten_dialog.get_by_role("textbox", name="Username")
        self.next_button = self.password_forgotten_dialog.get_by_role("button", name="Next")
        self.email_radio = self.password_forgotten_dialog.get_by_role("radio", name="Email")
        self.submit_button = self.password_forgotten_dialog.get_by_role("button", name="Submit")

    def request_token_via_email(self, username):
        self.username_input.fill(username)
        self.next_button.click()
        self.email_radio.click()
        self.submit_button.click()
