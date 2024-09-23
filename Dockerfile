# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

FROM mcr.microsoft.com/playwright/python:v1.37.0-jammy AS download

ENV \
    KUBECTL_VERSION="v1.30.5" \
    HELM_VERSION="v3.16.1"

RUN apt-get -qq update \
    && apt-get --assume-yes --verbose-versions --no-install-recommends install \
      curl=7.81.0-1ubuntu1.* \
    && rm -fr /var/lib/apt/lists/* /var/cache/apt/archives/*

RUN curl -LO "https://dl.k8s.io/release/${KUBECTL_VERSION}/bin/linux/amd64/kubectl" \
    && curl -LO "https://get.helm.sh/helm-${HELM_VERSION}-linux-amd64.tar.gz" \
    && tar -zxvf helm-${HELM_VERSION}-linux-amd64.tar.gz \
    && chmod +x kubectl linux-amd64/helm

FROM mcr.microsoft.com/playwright/python:v1.37.0-jammy AS build

WORKDIR /e2e/
COPY ./Pipfile .
COPY ./Pipfile.lock .
RUN pip install --no-cache-dir pipenv==2024.0.1 && \
    pipenv sync --system && \
    playwright install --with-deps

FROM build AS test

COPY --from=download /kubectl /linux-amd64/helm /usr/local/bin/

WORKDIR /e2e/

COPY . .
COPY ./entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["pytest", "--verbose", "--showlocals"]
