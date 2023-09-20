import re

from ..common.base import BasePage, expect


class OnDeviceBlockPage(BasePage):
    # navigate() not defined because logic is dependent on number of previous logins.
    # Only tests can have that info and should handle that.
    def set_content(self, *args, **kwargs):
        super().set_content(*args, **kwargs)
        blocked_msg = re.compile("Too many failed login.*device",
                                 re.IGNORECASE
                                 )
        self.device_blocked_message = self.page.get_by_text(blocked_msg)

    def is_displayed(self):
        expect(self.device_blocked_message).to_be_visible()


class OnIPBlockPage(BasePage):
    # navigate() not defined because logic is dependent on number of previous logins.
    # Only tests can have that info and should handle that.
    def set_content(self, *args, **kwargs):
        super().set_content(*args, **kwargs)
        blocked_msg = re.compile("Too many failed login.*IP",
                                 re.IGNORECASE
                                 )
        self.ip_blocked_message = self.page.get_by_text(blocked_msg)

    def is_displayed(self):
        expect(self.ip_blocked_message).to_be_visible()
