# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

FROM mcr.microsoft.com/playwright/python:v1.49.1-noble as build
WORKDIR /e2e/
COPY ./Pipfile .
COPY ./Pipfile.lock .
RUN pip install --no-cache-dir pipenv==2024.0.1 && \
    pipenv sync --system && \
    playwright install --with-deps

FROM build as test
WORKDIR /e2e/
COPY . .
COPY ./entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["pytest", "--verbose", "--showlocals"]
