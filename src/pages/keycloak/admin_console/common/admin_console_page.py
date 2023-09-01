from ....common.base import BasePage
from .header import Header


class AdminConsolePage(BasePage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header = Header(self.page.get_by_role("banner"))
