# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

ARG UCS_BASE_IMAGE_TAG=0.13.1-build-2024-09-05
ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/components/ucs-base-image/ucs-base-520


ARG WORKDIR="/app"

FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG} as build
ARG WORKDIR
WORKDIR ${WORKDIR}

RUN apt-get --assume-yes --verbose-versions --no-install-recommends install \
      python3-pip=23.* \
    && rm -fr /var/lib/apt/lists/* /var/cache/apt/archives/*

ENV \
    PATH="/home/${USER}/.local/bin:${PATH}" \
    PYTHONPATH="." \
    WEB_CONCURRENCY=1 \
    # Do not buffer `stdout`
    PYTHONUNBUFFERED=1 \
    # Do not create `.pyc` files
    PYTHONDONTWRITEBYTECODE=1 \
    # Do not ask questions
    POETRY_NO_INTERACTION=1 \
    # Put .venv inside source folder
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    # Cache of poetry
    POETRY_CACHE_DIR=/tmp/poetry_cache

# install Poetry
RUN pip3 install --break-system-packages --no-cache-dir poetry==1.6.1

# copy source code
COPY ./testing-api/src ${WORKDIR}/src

COPY testing-api/poetry.lock \
     testing-api/pyproject.toml \
     ${WORKDIR}/

# install dependencies
RUN poetry install --only main

# Stage 2: final image
FROM build as final
ARG WORKDIR
WORKDIR ${WORKDIR}

COPY --from=build ${WORKDIR} ${WORKDIR}

# run
ENTRYPOINT ["./.venv/bin/python3", "-m", "testing_api.main"]
