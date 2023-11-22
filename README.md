# Disclaimer - Work in progress

The repository you are looking into is work in progress.

It contains proof of concept and preview builds in development created in context of the [openDesk](https://gitlab.opencode.de/bmi/souveraener_arbeitsplatz/info) project.

The repository's content provides you with first insights into the containerized cloud IAM from Univention, derived from the UCS appliance.

# End-to-end tests used by the SouvAP Dev team

## Requirements

Make sure to have `pipenv` available, see <https://pipenv.pypa.io/en/latest/>.

## Installation

The installation is only needed once.

```
pipenv sync
pipenv shell

playwright install  # installs required browsers
```

## How to run tests

Then just run the following command.

```
pipenv shell

pytest
```

This will use the default settings for environment URL, login, etc. You can change
these settings by passing command line options. The available command line options
can be seen [here](tests/conftest.py).

So you can do the following to run the portal tests, for example:

```
pytest --username <my_user> --password <my_password> \
       --notifications-api-base-url <custom_notifications_api_base_url> \
       --portal-base-url <custom_portal_base_url> tests/portal
```

We use the `pytest-playwright` plugin, and it exposes useful command
line options for running end-to-end tests. See [all available options](https://playwright.dev/python/docs/test-runners).

Here are some useful ones:

1. `--headed`: Run tests in headed mode.
2. `--slowmo`: Run tests in slow motion e.g. `--slowmo 500`
3. `--video`: Capture video e.g. `--video on`
4. `--browser`: Use a specific browser `--browser firefox`

### Running with `docker`

```
docker build -t e2e:latest .
docker run -it --network="host" e2e:latest pytest
```

## For test engineers

We use the page object model in our tests. The page objects are in `src/umspages`.

You can pip install the page objects as a package using

```
pip install -e .
```

While this is not strictly necessary to run the tests (`pytest` finds the necessary
packages using the `[tool.pytest.ini_options]` in `pyproject.toml`), this will
help the IDE in autocompletion etc., and generally improve the development
experience.

We have a [guide on writing Page Objects, tests and fixtures](guidelines.md).

## Available tests

The brief description of every test in this repo can be found [here](tests.md).

## Processes

Our test management process is documented [here](https://univention.gitpages.knut.univention.de/customers/dataport/team-souvap/testing/test-management.html).
