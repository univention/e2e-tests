import pytest
from umspages.portal.home_page.logged_in import HomePageLoggedIn
from umspages.portal.home_page.logged_out import HomePageLoggedOut
from umspages.portal.login_page import LoginPage


@pytest.fixture()
def username(pytestconfig):
    return pytestconfig.option.username


@pytest.fixture()
def password(pytestconfig):
    return pytestconfig.option.password


@pytest.fixture()
def admin_username(pytestconfig):
    return pytestconfig.option.admin_username


@pytest.fixture()
def admin_password(pytestconfig):
    return pytestconfig.option.admin_password


@pytest.fixture()
def portal_base_url(pytestconfig):
    return pytestconfig.getoption("--portal-base-url")


@pytest.fixture()
def browser_context_args(browser_context_args, portal_base_url):
    browser_context_args["base_url"] = portal_base_url
    return browser_context_args


@pytest.fixture()
def navigate_to_home_page_logged_out(page):
    home_page_logged_out = HomePageLoggedOut(page)
    home_page_logged_out.navigate()
    return page


@pytest.fixture()
def navigate_to_login_page(page):
    login_page = LoginPage(page)
    login_page.navigate()
    return page


@pytest.fixture()
def navigate_to_saml_login_page(page):
    login_page = LoginPage(page)
    login_page.navigate_saml()
    return page


@pytest.fixture()
def navigate_to_home_page_logged_in(page, username, password):
    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_in.navigate(username, password)
    return page


@pytest.fixture()
def navigate_to_home_page_logged_in_as_admin(page, admin_username, admin_password):
    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_in.navigate(admin_username, admin_password)
    return page
