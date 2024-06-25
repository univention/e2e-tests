#!/bin/sh

# Check if PYTEST_ADDOPTS is already set
if [ -z "$PYTEST_ADDOPTS" ]; then
    # Set PYTEST_ADDOPTS based on NAMESPACE presence
    if [ -n "$NAMESPACE" ]; then
        export PYTEST_ADDOPTS="-m acceptance_environment --admin-username default.admin --admin-password $ADMIN_PASSWORD --username default.user --password $USER_PASSWORD --udm-admin-username cn=admin --udm-admin-password $UDM_ADMIN_PASSWORD --num-ip-block 7 --release-duration 1 --portal-base-url https://portal.$NAMESPACE.gaia.open-desk.cloud/univention/portal/"
    # else if PORTAL_BASE_URL
    elif [ -n "PORTAL_BASE_URL" ]; then
        export PYTEST_ADDOPTS="-m acceptance_environment --admin-username default.admin --admin-password $ADMIN_PASSWORD --username default.user --password $USER_PASSWORD --udm-admin-username cn=admin --udm-admin-password $UDM_ADMIN_PASSWORD --num-ip-block 7 --release-duration 1 --portal-base-url $PORTAL_BASE_URL"
    else
        export PYTEST_ADDOPTS="-m development_environment --admin-username default.admin --admin-password univention --username default.user --password univention --udm-admin-username cn=admin --udm-admin-password univention --num-ip-block 7 --release-duration 1 --portal-base-url http://localhost:8000/univention/portal/"
    fi
fi

exec "$@"
