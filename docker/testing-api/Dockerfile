# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

ARG UCS_BASE_IMAGE_TAG=5.2.7-build.20261126@sha256:b3ea4f3c1bcf55d860dd7e5b1643822f10d56dff1a9c2a83d7a3c80e45f22d16
ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base

ARG WORKDIR="/app"

FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG} AS build
ARG WORKDIR
WORKDIR ${WORKDIR}

COPY --from=ghcr.io/astral-sh/uv:0.13.9@sha256:d3b601f0c7b118bc1753febf7c41cc80981df678445e0254284eecf84db79a7d /uv /uvx /usr/local/bin/

ENV \
    # uv downloads the newest Python it knows, which the locked wheels may not cover yet
    UV_PYTHON="3.14" \
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
