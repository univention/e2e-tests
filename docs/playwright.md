# Playwright usage


## `BrowserContext`

Playwright has the concept of a `BrowserContext` which represents a fresh
session in the web browser.

Our test suite does customize the `BrowserContext` so that it is pre-configured:

- It uses `en-US` to select the default language.
- The time zone is set to `Europe/Berlin`.
- Cookies are injected so that the cookie banner is accepted by default.

The implementation is in the fixtures called `browser_context_args`. This can be
customized via all available fixture scopes in Pytest.

Pointers:

- [Playwright docs](https://playwright.dev/python/docs/test-runners#fixtures)
- [Example implementation](../tests/portal/conftest.py)


## Locating elements - prefer `get_by_role`

Using `get_by_role` to locate form elements is the closest way to how users
perceive the user interface. Compare the [Playwright
documentation](https://playwright.dev/python/docs/locators#locate-by-role)
regarding this topic.

If the usage of `get_by_role` does not work, double check if there is an
accessibility bug in the user interface before switching to other mechanisms
like the `data-testid` approach.
