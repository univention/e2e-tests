#!/bin/sh

: "${ADMIN_PASSWORD:=univention}"
: "${ADMIN_USERNAME:=default.admin}"
: "${MARKER:=development_environment}"
: "${PORTAL_CENTRAL_NAVIGATION_SECRET:=univention}"
: "${PORTAL_BASE_URL:=http://localhost:8000/univention/portal/}"
: "${UDM_ADMIN_PASSWORD:=univention}"
: "${UDM_ADMIN_USERNAME:=cn=admin}"
: "${USER_PASSWORD:=univention}"
: "${USER_USERNAME:=default.user}"
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

    export PYTEST_ADDOPTS="-m ${MARKER} --admin-username ${ADMIN_USERNAME} --admin-password ${ADMIN_PASSWORD} --username ${USER_USERNAME} --password ${USER_PASSWORD} --udm-admin-username ${UDM_ADMIN_USERNAME} --udm-admin-password ${UDM_ADMIN_PASSWORD} --portal-central-navigation-secret ${PORTAL_CENTRAL_NAVIGATION_SECRET} --num-ip-block 7 --release-duration 1 --portal-base-url ${PORTAL_BASE_URL} --email-test-api-username=${EMAIL_TEST_API_USERNAME} --email-test-api-password=${EMAIL_TEST_API_PASSWORD} --email-test-api-base-url=${EMAIL_TEST_API_BASE_URL}"
fi

exec "$@"
