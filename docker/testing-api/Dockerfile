# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

ARG UCS_BASE_IMAGE_TAG=5.2.7-build.20261112@sha256:583b21f19a9078a84b2832a316e3826dee06b7a346b352e3e49971c64ea4984b
ARG UCS_BASE_IMAGE=gitregistry.knut.univention.de/univention/dev/projects/ucs-base-image/ucs-base

ARG WORKDIR="/app"

FROM ${UCS_BASE_IMAGE}:${UCS_BASE_IMAGE_TAG} AS build
ARG WORKDIR
WORKDIR ${WORKDIR}

COPY --from=ghcr.io/astral-sh/uv:0.13.7@sha256:96f40d3904aad8d0bd010539001d36c8e2188b981e1334471a90c4a1d93bb490 /uv /uvx /usr/local/bin/

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
