FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy as build
WORKDIR /e2e/
COPY ./Pipfile .
COPY ./Pipfile.lock .
RUN pip install --no-cache-dir pipenv && \
    pipenv sync --system && \
    playwright install --with-deps

FROM build as test
WORKDIR /e2e/
COPY . .
CMD ["pytest"]
