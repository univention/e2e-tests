# Test Cases

Guideline and hints regarding the implementation of test cases.


## Multiple assertions

Ideally a test case should check one thing and be structured as follows:

1. Prepare
2. Take action
3. Check result

Having multiple asserts potentially mixed up with interim steps does mean that a
failing assertion will hide the state of all following ones.

The following strategies should be applied to improve the situation.


### Split if reasonably possible

If *reasonably* possible, then split the test case into two tests or more tests.

Consider the usage of Pytest's fixtures to prepare once and use the result in
multiple test cases.

Consider the usage of a class to group related cases together. Be reasonable
about the complexity which this may introduce, compare the "Avoid" example
below.

The following example shows a split which did work out without adding too much
complexity. The setup is done once for all checks. Be aware that this could also
have been done based on a `class`.

```python
@pytest.fixture(scope="module")
def logged_in_cookies(browser, browser_context_args, admin_username, admin_password):
    context = browser.new_context(**browser_context_args)
    page = context.new_page()

    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(admin_username, admin_password)

    home_page_logged_in = HomePageLoggedIn(page)
    home_page_logged_in.assert_logged_in()

    cookies = page.context.cookies()
    return cookies

def test_cookie_hardening_sets_samesite(logged_in_cookies):
    umc_session_cookie = _get_cookie(logged_in_cookies, "UMCSessionId")
    assert umc_session_cookie["sameSite"] == "Strict"

def test_cookie_hardening_sets_secure(logged_in_cookies):
    umc_session_cookie = _get_cookie(logged_in_cookies, "UMCSessionId")
    assert umc_session_cookie["secure"] is True

def test_cookie_hardening_does_not_set_expires(logged_in_cookies):
    umc_session_cookie = _get_cookie(logged_in_cookies, "UMCSessionId")
    assert umc_session_cookie["expires"] == -1

def _get_cookie(cookies, name):
    return [c for c in cookies if c["name"] == name][0]
```


### Use the `subtests` fixture

The `subtests` fixture allows to capture multiple states in a test case. It can
be used as a decorator:

```python
def test_example(subtests):

    with subtests.test(msg="First check will fail"):
        assert False

    with subtests.test(msg="First check will pass"):
        assert True
```


### Avoid - Too complex due to split

The following example shows a split based on Pytest's fixtures and a class
grouping it all together.

We found this result to be too complex and did prefer to user `subtests` in this
case. We were not able to confidently judge if this code will be stable or
flaky based on the implementation.

```python
class TestUserRequestsPasswordForgottenLinkFromLoginPage:

    @pytest.fixture(scope="class")
    def page(self, browser, browser_context_args):
        browser_context_args = browser_context_args.copy()
        context = browser.new_context(**browser_context_args)
        page = context.new_page()
        yield page
        page.close()
        context.close()

    @pytest.fixture(scope="class", autouse=True)
    def request_password_link(self, page, user):
        login_page = LoginPage(page)
        login_page.navigate(cookies_accepted=True)
        login_page.forgot_password_link.click()

        password_forgotten_page = PasswordForgottenPage(page)
        password_forgotten_page.request_token_via_email(user.properties["username"])

    def test_notification_pops_up(self, page):
        password_forgotten_page = PasswordForgottenPage(page)
        expect(password_forgotten_page.popup_notification_container).to_be_visible()
        notification = password_forgotten_page.popup_notification_container.notification(0)

        expect(notification).to_contain_text("Successfully sent Token")

    def test_set_new_password_page_is_displayed(self, page):
        set_new_password_page = SetNewPasswordPage(page)
        assert set_new_password_page.is_displayed()

    @pytest.fixture(scope="class")
    def link_with_token(self, email_test_api, user):
        link_with_token = get_password_reset_link_with_token(
            email_test_api, user.properties["PasswordRecoveryEmail"])
        return link_with_token

    def test_email_with_password_reset_link_has_been_sent(self, link_with_token):
        assert link_with_token

    @pytest.fixture(scope="class")
    def set_new_password(self, page, link_with_token, faker):
        page.goto(link_with_token)
        new_password = faker.password()
        set_new_password_page = SetNewPasswordPage(page)
        set_new_password_page.set_new_password(password=new_password)
        return new_password

    def test_link_can_be_used_to_set_a_new_password(self, page, set_new_password):
        set_new_password_page = SetNewPasswordPage(page)
        expect(set_new_password_page.password_change_successful_dialog).to_be_visible()

    def test_login_with_new_password_is_possible(self, page, user, set_new_password):
        new_password = set_new_password
        assert_user_can_log_in(page, user.properties["username"], new_password)
```
