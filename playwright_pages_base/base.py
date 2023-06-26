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
        self.page = page

    def navigate(self, *args, **kwargs):
        """Should navigate to this page"""
        raise NotImplementedError

    def navigate_to(self, target, *args, **kwargs):
        """Should navigate to target, given we are on this page"""
        raise NotImplementedError

    def is_displayed(self):
        """Checks if the page corresponding to this Page Object is displayed
        in the Playwright Page (browser tab).
        """
        raise NotImplementedError

    def get_new_tab(self, clickable):
        with self.page.expect_popup() as new_page_info:
            clickable.click()
        new_page = new_page_info.value
        return new_page


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
