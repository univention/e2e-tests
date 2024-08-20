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

from playwright.sync_api import Locator, Page, expect as playwright_expect


def expect(actual, *args, **kwargs):
    """This method is just like Playwright's expect(), but can also handle page objects and parts"""
    if isinstance(actual, BasePage):
        return playwright_expect(actual.page, *args, **kwargs)
    elif isinstance(actual, BasePagePart):
        return playwright_expect(actual.page_part_locator, *args, **kwargs)
    return playwright_expect(actual, *args, **kwargs)


class BasePage:
    """
    All full pages (i.e. which are not page parts) should be derived from this class.
    Methods that are common to full pages (as apposed to page parts) should go here.

    You can do page assertions directly by using expect() from playwright_pages_base
    instead of the vanilla expect() supplied by Playwright

    ```
    from playwright_pages_base import expect, BasePage

    class MyPage(BasePage):
        pass

    def some_test(page):
        my_page = MyPage(page)
        my_page.navigate()
        expect(my_page).to_have_title(...)
    ```
    """

    def __init__(self, page: Page):
        self.set_content(page)

    def set_content(self, page):
        """This method should be used to define page elements and page parts.
        It allows to change the tab and redefine the elements/page parts based
        on the new tab.
        """
        self.page = page

    def navigate(self, *args, **kwargs):
        """Should navigate to this page from a well-defined root page using a
        canonical path. Note that this may open new tabs, since the root page
        and this page may be displayed in different tabs. In this case, you
        should call set_content() to ensure that this page object is based on the
        correct tab.
        """
        raise NotImplementedError

    def is_displayed(self) -> bool:
        """
        Check if the page is displayed.

        Checks if the page corresponding to this Page Object is displayed
        in the Playwright Page (browser tab).
        """
        raise NotImplementedError

    def assert_is_displayed(self) -> None:
        """
        Asserts that this page is displayed.
        """
        assert self.is_displayed()

    def get_new_tab(self, clickable):
        """Clicking on some clickable elements opens a new tab/window.
        This method is used to click on such an element and retrieve the new tab/window.
        """
        with self.page.expect_popup() as new_page_info:
            clickable.click()
        new_page = new_page_info.value
        return new_page

    @staticmethod
    def reveal_area(area, clickable):
        """Method that ensures that a collapsible area (could be a dropdown or sliding menu)
        is in the revealed state.

        Parameters
        ----------
        area : BasePagePart or Locator
        clickable: Locator
                   Clickable element that is responsible for opening and closing area
        """
        try:
            expect(area).to_be_hidden()
        except AssertionError:
            pass
        else:
            clickable.click()
            expect(area).to_be_visible()

    @staticmethod
    def hide_area(area, clickable):
        """Method that ensures that a collapsible area (could be a dropdown or sliding menu)
        is in the collapsed state.

        Parameters
        ----------
        area : BasePagePart or Locator
        clickable: Locator
                   Clickable element that is responsible for opening and closing area
        """
        try:
            expect(area).to_be_visible()
        except AssertionError:
            pass
        else:
            clickable.click()
            expect(area).to_be_hidden()

    def upload_files(self, files, clickable):
        """Method to upload a file

        Parameters
        ----------
        files : str or pathlib.Path (or list thereof)
        clickable: Locator
                   Clickable element that is responsible for opening the file picker
        """
        with self.page.expect_file_chooser() as file_chooser_info:
            clickable.click()
        file_chooser = file_chooser_info.value
        file_chooser.set_files(files)


class BasePagePart:
    """
    All classes representing page parts should be derived from this class

    The page containing the page part should store a reference to the part page as follows

    ```
    class Header(BasePagePart):
        ...

    class MyPage(BasePage):
        def __init__(self, *args, **kwargs)
            super().__init__(self, *args, **kwargs)
            self.header = Header(self.page.locator(some_locator))
    ```

    Then, you can get do the following:

    ```
    from playwright_pages_base import expect

    def some_test(page):
        my_page = MyPage(page)
        expect(my_page.header).is_visible()
    ```
    """

    def __init__(self, page_part_locator):
        if not isinstance(page_part_locator, Locator):
            raise ValueError(f"Locators must be of type Locator, got  {type(page_part_locator)}")
        self.page_part_locator = page_part_locator
