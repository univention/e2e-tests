import re

from playwright_pages_base.base import expect
from .base import HomePage
from ..login_page import LoginPage


class HomePageLoggedIn(HomePage):
    """This represents the logged in state of the portal's home page."""

    def set_content(self, *args, **kwargs):
        super().set_content(*args, **kwargs)
        self.umc_heading = self.page.get_by_text("Univention Management Console", exact=True)
        self.users_tile = self.page.get_by_role("link", name=re.compile("User New Tab|Users iFrame"))
        self.files_tile = self.page.get_by_role("link", name="Files New Tab")
        self.mail_tile = self.page.get_by_role("link", name="E-Mail New Tab")
        self.calendar_tile = self.page.get_by_role("link", name="Calendar New Tab")
        self.contacts_tile = self.page.get_by_role("link", name="Contacts New Tab")
        self.tasks_tile = self.page.get_by_role("link", name="Tasks New Tab")
        self.video_conference_tile = self.page.get_by_role("link", name="Ad hoc videoconference New Tab")
        self.projects_tile = self.page.get_by_role("link", name="Projects New Tab")
        self.activity_tile = self.page.get_by_role("link", name="Activity New Tab")

    def navigate(self, username, password):
        self.page.goto("/")
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
        else:
            login_page = LoginPage(self.page)
            login_page.navigate(cookies_accepted=True)
            login_page.is_displayed()
            login_page.login(username, password)
            self.reveal_area(self.right_side_menu, self.header.hamburger_icon)
            expect(self.right_side_menu.logout_button).to_be_visible()
            expect(self.right_side_menu.login_button).to_be_hidden()
        finally:
            self.hide_area(self.right_side_menu, self.header.hamburger_icon)

    def is_displayed(self):
        # TODO: There seems to be nothing that's necessarily common between the UCS and SouvAP envs
        # We resort to checking nothing here.
        pass

    def click_users_tile(self):
        self.users_tile.click()
