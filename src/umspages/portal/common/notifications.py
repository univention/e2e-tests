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

from ...common.base import BasePagePart  # type: ignore


class NotificationsContainer(BasePagePart):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.notifications = self.page_part_locator.locator(
            "//*[starts-with(@data-test, 'notification')]"
        )

    def notification(self, n):
        count = self.notifications.count()
        if n >= count:
            raise IndexError(
                f"You are trying to access the {n}th popup notification, "
                f"but here are only {count} popup notifications",
            )
        return NotificationElement(self.notifications.nth(n))


class NotificationDrawer(NotificationsContainer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.remove_all_button = self.page_part_locator.get_by_role(
            "button", name="Remove all"
        )
        self.no_notifications_heading = self.page_part_locator.get_by_text(
            "No notifications"
        )

    def click_remove_all_button(self):
        self.remove_all_button.click()


class PopupNotificationContainer(NotificationsContainer):
    pass


class NotificationElement(BasePagePart):
    """This represents a single notification element."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.close_button = self.page_part_locator.locator(
            "//*[contains(@data-test, 'closeNotification')]"
        )
        self.link = self.page_part_locator.get_by_role("link")
        self.title = self.page_part_locator.locator(
            "//div[@class='notification__title']"
        )
        self.details = self.page_part_locator.locator(
            "//div[@class='notification__description']"
        )

    def click_close_button(self):
        self.close_button.click()
