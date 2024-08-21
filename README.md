# Disclaimer - Work in progress

The repository you are looking into is work in progress.

It contains proof of concept and preview builds in development created in context of the [openDesk](https://gitlab.opencode.de/bmi/souveraener_arbeitsplatz/info) project.

The repository's content provides you with first insights into the containerized cloud IAM from Univention, derived from the UCS appliance.


# End-to-End Test Suite for Nubus


## About

This is the end-to-end test suite used for Nubus. It focuses on ensuring that
the Kubernetes based deployment of the included components functions as
expected.

This test suite complements existing test suites related to the various
components and their source code. It does not aim to verify all aspects of every
component, those checks are already included in the component focused test
suites.


## Detailed documentation

Detailed documentation is provided in the [docs](./docs) folder of this
repository.

This README serves as a starting point and a quick start guide for users of this
test suite.

Details about how to develop tests and which patterns to follow are also
captured within the [docs](./docs) folder.


## Getting started - Options

The easiest way to use the test suite is currently by setting everything up
locally on your machine.

There is also container based support. See the [Dockerfile](./Dockerfile) to get
an idea and the notes below. Usage is still a bit rough and has to be improved
before we switch to this as the suggested default approach.


## Getting started based on a local environment

### Requirements

Make sure to have a recent Python interpreter. We only verify that the one in
the container image works, the other versions are best-effort only.

Make sure to have `pipenv` available, see <https://pipenv.pypa.io/en/latest/>.

Verify like this:

```sh
pipenv --help
```

### Installation

The installation is only needed once:

```
# Installs everything from the Pipfile.lock.
pipenv sync

# Gives you a shell with the dependencies available.
pipenv shell

# Installs required browsers.
# This is a bit heavier and may take a bit of time.
playwright install
```

### How to run tests

#### Prepare

There is one preparatory step to enter the environment:

```sh
# Discover the needed configuration parameters.
#
# If you want to explicitly tell the namespace via an environment variable
export DEPLOY_NAMESPACE=your-nubus-deployment

# Look into the script to understand its preconditions and options
# in detail.
source ./discover-env-from-cluster.sh

# Enter the virtual environment with the dependencies
pipenv shell
```

#### Run

Run the tests:

```sh
# Our default run in CI
pytest -v -m acceptance_environment

# Repeat failed tests
pytest -v -m acceptance_environment --lf

# Select test by name
pytest -v -m acceptance_environment -k admin_invites

# Select by folder or file
pytest -v -m acceptance_environment tests/portal/test_selfservice.py
```

#### Playwright specifics

We use the `pytest-playwright` plugin, and it exposes useful command line
options for running end-to-end tests. See [all available
options](https://playwright.dev/python/docs/test-runners).

Here are frequently used ones:

1. `--headed`: Run tests in headed mode.
2. `--slowmo`: Run tests in slow motion e.g. `--slowmo 500`
3. `--video`: Capture video e.g. `--video on`
4. `--browser`: Use a specific browser `--browser firefox`


## Getting started based on a CI Pipeline

Go to the
[pipelines](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/-/pipelines)
of this repo and run the pipeline with the following variables:

- `TEST_PORTAL_BASE_URL`: The base URL of the portal to test. Example: `https://portal.uv-username.gaia.open-desk.cloud/univention/portal/`.

The pipeline will use the default secrets for Gaia. But you can override them by
setting `ADMIN_PASSWORD` and `PORTAL_CENTRAL_NAVIGATION_SECRET`.


## Getting started based on a container

Be aware, we don't have a smooth experience yet for this. There is no
configuration yet available to run this via docker compose.

### Build or pull the container

Building the container:

```shell
docker build -t local/e2e:latest .
docker run -it --network="host" local/e2e:latest
```

Pulling it from CI (only works in the internal network):

```shell
docker pull gitregistry.knut.univention.de/univention/customers/dataport/upx/e2e-tests/e2e-tests-runner:latest
docker run -it --network="host" gitregistry.knut.univention.de/univention/customers/dataport/upx/e2e-tests/e2e-tests-runner
```

The container uses `entrypoint.sh` to configure pytest, look into the file to
know what is going on.

Alternatively, you can directly test against the acceptance environment. In
order to get the preconfigured credentials, you should specify
`sovereign-workplace` in the `MASTER_PASSWORD_WEB_VAR` on openDesk pipeline.
Once finished, run the following command:

```shell
docker run -it --network="host" \
  -e NAMESPACE=uv-username \
  -e ADMIN_PASSWORD=secret \
  e2e:latest
```

You can always override the value of `PYTEST_ADDOPTS` generated by the
`entrypoint.sh` with the `-e` flag, and/or run a custom command. Example:

```shell
docker run -it --network="host" -e PYTEST_ADDOPTS="..." e2e:latest pytest --pdb
```

Or just override one (or many) of the `PYTEST_ADDOPTS` flags:

```shell
docker run -it --network="host" e2e:latest pytest --admin-password custom_password
```


## Available tests

The brief description of every test in this repo can be found [here](tests.md).


## Processes

Our test management process is documented
[here](https://univention.gitpages.knut.univention.de/customers/dataport/team-souvap/testing/test-management.html).
