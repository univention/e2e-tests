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

from playwright.sync_api import Page

from attrdict import AttrDict
from pom.base_page import BasePage


class ManageAnnouncementsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.add_button = page.locator('[role="button"]:visible', has_text='Add')

    @staticmethod
    def get_language_id(name):
        return {
            'en_US': '48',
        }[name]

    @staticmethod
    def get_severities_id(name):
        return {
            'info': '0',
            'warn': '1',
            'success': '2',
            'danger': '3'
        }[name]

    def is_announcement_on_page(self, announcement: AttrDict) -> bool:
        return self._page.locator(
            '[id*=' + announcement.properties.name + ']'
        ).is_visible()

    def add_announcement(self, announcement: AttrDict):
        self.add_button.click()

        self._page.locator('text=Internal').fill(
            announcement.properties.name
        )

        ###################
        # Fill content info
        ###################
        content_pane = self._page.locator('.umcTitlePane:visible', has_text='Content')

        # Fill title
        lang, title = list(announcement.properties.title.items())[0]
        lang_id = self.get_language_id(lang)
        content_pane.locator('.umcTextBox__downArrowButton:visible').locator("nth=0").click()
        self._page.locator('#umc_widgets_SuggestionBox_2_popup' + lang_id).click()
        content_pane.locator('#umc_widgets_TextBox_5').fill(title)

        # Fill message
        lang, msg = list(announcement.properties.message.items())[0]
        lang_id = self.get_language_id(lang)
        content_pane.locator('.umcTextBox__downArrowButton:visible').locator("nth=1").click()
        self._page.locator('#umc_widgets_SuggestionBox_3_popup' + lang_id).click()
        content_pane.locator('#umc_widgets_TextBox_6').fill(msg)

        ###################
        # Fill time
        ###################
        time_pane = self._page.locator('.umcTitlePane:visible', has_text='Time')

        ###################
        # Fill options
        ###################
        options_pane = self._page.locator('.umcTitlePane:visible', has_text='Options')

        if announcement.properties.needsConfirmation:
            options_pane.locator('input[name="needsConfirmation"]:visible').click()

        if announcement.properties.isSticky:
            options_pane.locator('input[name="isSticky"]:visible').click()

        severity_id = self.get_severities_id(announcement.properties.severity)
        options_pane.locator('.umcTextBox__downArrowButton:visible').click()
        owner_id = self._page.locator('.syntaxNewPortalAnnouncementSeverity').get_attribute('widgetid')
        self._page.locator('#' + owner_id + '_popup' + severity_id).click()

        ###################
        # Submit data
        ###################
        self._page.locator('[role="button"]').locator('[data-iconName="save"]').click()

    def remove_announcement(self, announcement: AttrDict):
        item = self._page.locator('[id*=' + announcement.properties.name + ']')
        item.locator('[role="checkbox"]').click()
        self._page.locator('[role="button"]:visible', has_text='Delete').click()
        self._page.locator('[role="dialog"]').locator('[role="button"]', has_text='Delete').click()

    def get_announcement_severity(self, announcement_name: str) -> str:
        '''
        return self._page.locator(
            '[id*=' + announcement_name + ']'
        ).is_visible()
        '''
        pass
