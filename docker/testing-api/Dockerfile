# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

ARG UCS_BASE_IMAGE_TAG=5.2.6-build.20260903@sha256:1ffe8002cb3e0f7c28ac4270825c4168df91970e237f9c7e10c3b8bf941b3573
ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base

ARG WORKDIR="/app"

FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG} AS build
ARG WORKDIR
WORKDIR ${WORKDIR}

COPY --from=ghcr.io/astral-sh/uv:0.12.10@sha256:2bb3ebca0a796a155094a27773d290c4b074572e6107f171d88d086682fd2500 /uv /uvx /usr/local/bin/

ENV \
    PATH="/home/${USER}/.local/bin:${PATH}" \
    PYTHONPATH="." \
    WEB_CONCURRENCY=1 \
    # Do not buffer `stdout`
    PYTHONUNBUFFERED=1 \
    # Do not create `.pyc` files
    PYTHONDONTWRITEBYTECODE=1

COPY testing-api/uv.lock \
    testing-api/pyproject.toml \
    ${WORKDIR}/

# Install dependencies only for smart layer caching
RUN uv sync --frozen --no-install-project --no-dev

# Copy source code
COPY ./testing-api/src ${WORKDIR}/src

# Install the application itself
RUN uv sync --frozen --no-dev

# Stage 2: final image
FROM build AS final
ARG WORKDIR
WORKDIR ${WORKDIR}

COPY --from=build ${WORKDIR} ${WORKDIR}

# run
ENTRYPOINT ["./.venv/bin/python3", "-m", "testing_api.main"]
