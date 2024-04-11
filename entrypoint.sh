#!/bin/sh

# Check if PYTEST_ADDOPTS is already set
if [ -z "$PYTEST_ADDOPTS" ]; then
    # Set PYTEST_ADDOPTS based on GAIA_NAMESPACE presence
    if [ -n "$GAIA_NAMESPACE" ]; then
        export PYTEST_ADDOPTS="-m acceptance_environment --admin-username default.admin --admin-password bbc4e12661caa3a903c1072bfb5d5bb461819ae9 --username default.user --password 517fdd0662ef3da1f1f93ddcef0d3a8d6b31b81f --udm-admin-username cn=admin --udm-admin-password e958ec347ebf4cd1959f4e8536dcedfc3fcea023 --num-ip-block 7 --release-duration 10 --portal-base-url https://portal.$GAIA_NAMESPACE.gaia.open-desk.cloud/univention/portal/"
    else
        export PYTEST_ADDOPTS="-m development_environment --admin-username default.admin --admin-password univention --username default.user --password univention --udm-admin-username cn=admin --udm-admin-password univention --num-ip-block 7 --release-duration 10 --portal-base-url http://localhost:8000/univention/portal/"
    fi
fi

exec "$@"
