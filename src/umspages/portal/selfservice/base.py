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

from ...common.base import expect
from ..common.portal_page import PortalPage
from ..login_page import LoginPage


class SelfservicePortal(PortalPage):
    """
    The selfservice portal is a separate portal focused on selfservice.

    It does provide functionality for password reset and also around account
    management.
    """

    def navigate(self):
        self.page.goto("/univention/selfservice/")

    def set_content(self, *args, **kwargs):
        super().set_content(*args, **kwargs)
        self.my_profile_tile = self.page.get_by_label("My Profile Same tab")
        self.protect_account_tile = self.page.get_by_label("Protect your account Same tab")

        # Typically only visible for anonymous users
        self.password_forgotten_tile = self.page.get_by_label("Password forgotten Same tab")

        # UMC tiles headline - Expected not to be there in default
        # configurations
        self.umc_tiles_headline = self.page.get_by_role("heading", name="Univention Management Console")

    def login(self, username, password):
        self.reveal_area(self.right_side_menu, self.header.hamburger_icon)
        expect(self.right_side_menu.login_button).to_be_visible()
        expect(self.right_side_menu.logout_button).to_be_hidden()
        self.right_side_menu.login_button.click(timeout=2000)

        login_page = LoginPage(self.page)
        login_page.login_with_retry(username, password)
        self.page.wait_for_url("/univention/selfservice/**", timeout=5000)
