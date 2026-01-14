# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

FROM mcr.microsoft.com/playwright/python:v1.57.0-noble@sha256:3de745b23fc4b33fccbcb3f592ee52dd5c80ce79f19f839c825ce23364e403c1 AS build
WORKDIR /e2e/
COPY ./Pipfile .
COPY ./Pipfile.lock .
RUN pip install --no-cache-dir pipenv==2024.0.1 && \
    pipenv sync --system && \
    playwright install --with-deps && \
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    chmod +x kubectl && \
    mv kubectl /usr/local/bin/kubectl

FROM build AS test
WORKDIR /e2e/
COPY . .
COPY ./entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["pytest", "--verbose", "--showlocals"]
