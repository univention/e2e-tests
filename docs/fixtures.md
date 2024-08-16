# Fixture Design Principles

## Fixtures which connect to APIs

Fixtures which do connect to an API like the UDM Rest API or the Maildev based
email API should verify the correctness of the configuration early on.

This gives fast feedback when using the test suite with incorrect credentials or
missing configuration.

See `email_test_api_session` for an example.

## Fixtures which represent Page Object Models

Since Playwright is tightly integrated with `pytest`, we need to decide what
`pytest` fixtures are responsible for and how it is to be used. Here are some
guidelines regarding that.

1. `pytest` fixtures usually shouldn't handle navigation logic. Use the page
   object's `navigate()` method instead.

2. Fixtures that used the `page` fixture should also return the playwright
   Page after performing the necessary actions. This is to ensure that the
   passing on various browser tabs to the test is explicit, instead of being
   done implicitly via the `page` fixture.

    ```
    @pytest.fixture
    def navigate_to_login_page(page):
        login_page = LoginPage(page)
        login_page.navigate()
        return page # Good

    # Explicit page/tab passed to test
    def test_something_on_login_page(navigate_to_login_page):
        page = navigate_to_login_page
        login_page = LoginPage(page)
        # Test something on login page

    @pytest.fixture
    def navigate_to_login_page(page):
        login_page = LoginPage(page)
        login_page.navigate()
        return  # Bad

    # Implicitly using the page fixture
    def test_something_on_login_page(page, navigate_to_login_page):
        login_page = LoginPage(page)
        # Test something on login page
    ```

3. Fixtures should try to use action terms in their names e.g. use
   `navigate_to_login_page` instead of just `login_page`. This is to prevent
   the name `login_page` from being taken, so that it can be used for the
   respective page object.

    ```
    @pytest.fixture
    def login_page(page):  # bad
        # login_page is taken, so we are forced to use the ambiguous this_page
        this_page = LoginPage(page)
        this_page.navigate()
        return page
    ```

4. Teardown shouldn't expect the `page` fixture to be in the same state as in
   setup time, as the test may navigate away from it. Try to always call
   `navigate()` on page objects used in teardown.
