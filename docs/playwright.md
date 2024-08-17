# Playwright usage

## Locating elements - prefer `get_by_role`

Using `get_by_role` to locate form elements is the closest way to how users
perceive the user interface. Compare the [Playwright
documentation](https://playwright.dev/python/docs/locators#locate-by-role)
regarding this topic.

If the usage of `get_by_role` does not work, double check if there is an
accessibility bug in the user interface before switching to other mechanisms
like the `data-testid` approach.
