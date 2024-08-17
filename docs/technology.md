# Technology and Tools

## Test suite

The test suite is based on `pytest`:

- [Pytest docs](https://docs.pytest.org/en/7.2.x/)

## Browser automation

Playwright is used for browser automation:

- [Playwright Documentation](https://playwright.dev/python/docs/intro)
- [Playwright API Reference](https://playwright.dev/python/docs/api/class-playwright)

The plugin `pytest-playwright` does provide ready made Pytest fixtures.

## HTTP based APIs

[Requests][requests-docs] is used to speak with HTTP based APIs where no
provided client is used.

[requests-docs]: https://docs.python-requests.org/en/latest/index.html

## Stub data

[Faker][faker-docs] is available and used in some places to provide generated
stub data. Note that Faker is integrated with Pytest through a
[plugin][faker-pytest], so that the generated data is deterministic.

[faker-docs]: https://faker.readthedocs.io/en/master/
[faker-pytest]: https://faker.readthedocs.io/en/master/pytest-fixtures.html
