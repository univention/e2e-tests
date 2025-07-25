#!/bin/sh
# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH


: "${ADMIN_PASSWORD:=univention}"
: "${ADMIN_USERNAME:=Administrator}"
: "${MARKER:=development_environment}"
: "${PORTAL_BASE_URL:=http://localhost:8000/univention/portal/}"
: "${EMAIL_TEST_API_USERNAME:=user}"
: "${EMAIL_TEST_API_PASSWORD:=password}"
: "${EMAIL_TEST_API_BASE_URL:=http://localhost:8001/email}"

# Check if PYTEST_ADDOPTS is already set
if [ -z "$PYTEST_ADDOPTS" ]; then
    # Set PYTEST_ADDOPTS based on NAMESPACE presence
    if [ -n "$NAMESPACE" ]; then
        MARKER="acceptance_environment"
        PORTAL_BASE_URL="https://portal.$NAMESPACE.gaia.open-desk.cloud/univention/portal/"
        # else if PORTAL_BASE_URL
    elif [ -n "$PORTAL_BASE_URL" ]; then
        MARKER="acceptance_environment"
    fi

    export PYTEST_ADDOPTS="-m ${MARKER} --admin-password ${ADMIN_PASSWORD} --num-ip-block 7 --release-duration 1 --portal-base-url ${PORTAL_BASE_URL} --email-test-api-username=${EMAIL_TEST_API_USERNAME} --email-test-api-password=${EMAIL_TEST_API_PASSWORD} --email-test-api-base-url=${EMAIL_TEST_API_BASE_URL}"
fi

# NOTE: This will show secrets in the test logs.
if [ -n "${DEBUG_PYTEST_ADDOPTS}" ]
then
    echo "PYTEST_ADDOPTS"
    echo "${PYTEST_ADDOPTS}"
fi

exec "$@"
