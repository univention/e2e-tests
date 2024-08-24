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

import re

from ..common.base import BasePage, expect


class OnDeviceBlockPage(BasePage):
    # navigate() not defined because logic is dependent on number of previous logins.
    # Only tests can have that info and should handle that.
    def set_content(self, *args, **kwargs):
        super().set_content(*args, **kwargs)
        blocked_msg = re.compile("Too many failed login.*device", re.IGNORECASE)
        self.device_blocked_message = self.page.get_by_text(blocked_msg)

    def is_displayed(self):
        expect(self.device_blocked_message).to_be_visible()


class OnIPBlockPage(BasePage):
    # navigate() not defined because logic is dependent on number of previous logins.
    # Only tests can have that info and should handle that.
    def set_content(self, *args, **kwargs):
        super().set_content(*args, **kwargs)
        blocked_msg = re.compile("Too many failed login.*IP", re.IGNORECASE)
        self.ip_blocked_message = self.page.get_by_text(blocked_msg)

    def is_displayed(self):
        expect(self.ip_blocked_message).to_be_visible()
