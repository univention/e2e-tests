FROM mcr.microsoft.com/playwright/python:v1.37.0-jammy as build
WORKDIR /e2e/
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && playwright install --with-deps

FROM build as test
WORKDIR /e2e/
COPY . .
CMD ["pytest"]
