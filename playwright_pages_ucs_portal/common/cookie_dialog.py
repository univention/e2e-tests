from playwright_pages_base.base import BasePagePart


class CookieDialog(BasePagePart):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.accept_button = self.page_part_locator.get_by_role("button", name="Accept")

    def click_accept_button(self):
        self.accept_button.click()
