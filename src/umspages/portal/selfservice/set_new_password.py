# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

from ...common.base import BasePage


class SetNewPasswordPage(BasePage):
    """
    This is the page one reaches when using the "password reset" functionality.

    This page can only be reached in the following ways:

    1. Using the "Password forgotten" link in the `LoginPage`. After requesting
       the token via e.g. email successfully this page will be shown.

    2. Using one of the links from the email sent. Apart from (1) this email
       can also be triggered by an administrator or through the Selfservice
       portal.
    """

    def set_content(self, *args, **kwargs):
        super().set_content(*args, **kwargs)
        self.set_new_password_dialog = self.page.get_by_role("dialog", name="Set new password")
        self.new_password_box = self.set_new_password_dialog.get_by_role("textbox", name="New password")
        self.retype_password_box = self.set_new_password_dialog.get_by_test_id("retype-password-box")

        # TODO: Switch to "get_by_role" once the frontend fix is released
        # See: https://git.knut.univention.de/univention/components/univention-portal/-/merge_requests/447

        # self.retype_password_box = self.page.get_by_role("textbox", name="New password (retype)")

        self.submit_button = self.set_new_password_dialog.get_by_role("button", name="Change password")
        self.password_change_successful_dialog = self.page.get_by_role("dialog", name="Password change successful")

    def navigate(self, url):
        self.page.goto(url)

    def is_displayed(self):
        self.set_new_password_dialog.wait_for(state="visible", timeout=500)
        return True

    def set_new_password(self, password):
        self.new_password_box.fill(password)
        self.retype_password_box.fill(password)
        self.submit_button.click()
