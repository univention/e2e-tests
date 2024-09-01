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

from ...common.base import expect
from ..login_page import LoginPage
from .base import SelfservicePortal


class SelfservicePortalLoggedIn(SelfservicePortal):
    """
    This represents the logged out state of the selfservice portal
    """

    def navigate(self, username, password):
        self.page.goto("/univention/selfservice/")
        try:
            expect(self.cookie_dialog).to_be_visible()
        except AssertionError:
            pass
        else:
            self.accept_cookies()
        self.reveal_area(self.right_side_menu, self.header.hamburger_icon)
        try:
            expect(self.right_side_menu.login_button).to_be_visible()
        except AssertionError:
            expect(self.right_side_menu.logout_button).to_be_visible()
            self.hide_area(self.right_side_menu, self.header.hamburger_icon)
            return

        self.reveal_area(self.right_side_menu, self.header.hamburger_icon)
        expect(self.right_side_menu.login_button).to_be_visible()
        expect(self.right_side_menu.logout_button).to_be_hidden()
        self.right_side_menu.login_button.click(timeout=2000)

        login_page = LoginPage(self.page)
        login_page.login(username, password)
