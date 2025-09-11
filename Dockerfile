# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

FROM mcr.microsoft.com/playwright/python:v1.55.0-noble@sha256:640d578aae63cfb632461d1b0aecb01414e4e020864ac3dd45a868dc0eff3078 AS build
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
