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
the container image (atm, 3.12.3) works, the other versions are best-effort only.

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

Run the tests locally:

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
5. `--tracing=retain-on-failure`: Saves trace files in `test-results/` when tests fail.
6. `--video=retain-on-failure`: Saves video in `test-results/`  when tests fail.


## Getting started based on a CI Pipeline (Recommended)

Go to the
[pipelines](https://git.knut.univention.de/univention/customers/dataport/upx/e2e-tests/-/pipelines)
of this repo and run the pipeline with the following variables:

- `TEST_PORTAL_BASE_URL`: The base URL of the portal to test. Example: `https://portal.uv-username.gaia.open-desk.cloud/univention/portal/`.

The pipeline will use the default secrets for Gaia. But you can override them by
setting `ADMIN_PASSWORD`.


## Getting started based on a container

The easiest way to run the e2e tests in a containerized environment is using docker compose.

### Using docker-compose (Recommended)

#### Option 1: Build local container

Build and run the tests using a locally built container:

```shell
docker-compose run --rm --build test
```

#### Option 2: Pull from remote registry

Use a pre-built container from the registry (only works in the internal network):

```shell
# Use latest version
docker-compose run --rm test

# Use a specific version
IMAGE_TAG=v1.2.3 docker-compose run --rm --no-build test
```

#### Configure environment

You have to configure the test run with environment variables:

```shell
RELEASE_NAME=my-release DEPLOY_NAMESPACE=my-namespace IMAGE_TAG=latest docker-compose up test
```

Available environment variables:
- `DEPLOY_NAMESPACE`: (required) Kubernetes namespace to test
- `RELEASE_NAME`: (optional, default: `nubus`) Name of the release to test
- `IMAGE_TAG`: (optional, default: `latest`) Container image tag to use
- `KUBECONFIG`: (optional, default: `~/.kube/config`) Path to kubeconfig file to mount in container

### Manual container usage (Advanced)

If you need more control, you can still run containers manually:

Building the container:

```shell
docker build -t local/e2e:latest .
docker run -it --network="host" local/e2e:latest
```

Pulling from CI:

```shell
docker pull gitregistry.knut.univention.de/univention/customers/dataport/upx/e2e-tests/e2e-tests-runner:latest
docker run -it --network="host" gitregistry.knut.univention.de/univention/customers/dataport/upx/e2e-tests/e2e-tests-runner
```

The container uses `entrypoint.sh` to configure pytest, look into the file to
know what is going on.


## Available tests

The brief description of every test in this repo can be found [here](tests.md).


## Processes

Our test management process is documented
[here](https://univention.gitpages.knut.univention.de/customers/dataport/team-souvap/testing/test-management.html).
