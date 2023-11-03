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

from ...common.base import BasePagePart  # type: ignore


class Header(BasePagePart):
    """This represents the portal's top navigation header bar."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bell_icon = self.page_part_locator.get_by_role(
            "button", name=re.compile("^Notifications")
        )
        self.hamburger_icon = self.page_part_locator.locator(
            "#header-button-menu"
        )

    def click_bell_icon(self):
        self.bell_icon.click()

    def click_hamburger_icon(self):
        self.hamburger_icon.click()
