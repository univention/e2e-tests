# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

# This file tries to discover the credentials via "kubectl" out of a given
# deployment.
#
# Usage:
#
# 1. Make sure that you have your Kubernetes configuration selected, e.g. the
#    correct cluster and namespace.
#
#    Regarding the namespace, either use "kubens" or set the variable
#    "DEPLOY_NAMESPACE".
#
# 2. Adjust the release name if it is not "nubus" by setting the variable
#    "RELEASE_NAME".
#
# 3. Source this file to set the environment variables:
#
#        source discover-env-from-cluster.sh
#
# 4. Check the output.


# If no namespace is provided, then try to discover the namespace via "kubectl".
# The parameter "--minify" is important, it ensures that we only get the
# configuration related to the currently selected context.
: "${DEPLOY_NAMESPACE:=$(kubectl config view --minify -o jsonpath='{..namespace}')}"

# The release name is typically "nubus". In openDesk it is currently "ums". In
# general it can be freely chosen.
: "${RELEASE_NAME:=nubus}"


echo "Namespace: ${DEPLOY_NAMESPACE}"
echo "Release name: ${RELEASE_NAME}"
echo "API Server: $(kubectl config view --minify -o jsonpath='{..server}')"
echo "Cluster: $(kubectl config view --minify -o jsonpath='{.contexts[0].context.cluster}')"


# Discover secrets and the domain.
#
# These commands depend on the Nubus deployment and will have to be kept in sync
# with the progressing Nubus chart.
default_admin_password=$(kubectl get secret -n "${DEPLOY_NAMESPACE}" "${RELEASE_NAME}-nubus-credentials" -o jsonpath="{.data.administrator_password}" | base64 -d)
portal_hostname=$(kubectl get ingress -n "${DEPLOY_NAMESPACE}" "${RELEASE_NAME}-portal-server" -o jsonpath="{.spec.rules[0].host}")
portal_base_url=https://$portal_hostname
keycloak_base_url=https://$(kubectl get ingress -n "${DEPLOY_NAMESPACE}" "${RELEASE_NAME}-keycloak-extensions-proxy" -o jsonpath="{.spec.rules[0].host}")
ldap_base_dn=$(kubectl -n "${DEPLOY_NAMESPACE}" get configmaps "${RELEASE_NAME}-ldap-server-primary" -o jsonpath="{.data.LDAP_BASEDN}")

email_test_api_base_url=$(kubectl get --ignore-not-found ingress -n "${DEPLOY_NAMESPACE}" maildev -o jsonpath="{.spec.rules[0].host}")
if [ -n "$email_test_api_base_url" ]
then
    email_test_api_base_url="https://${email_test_api_base_url}"
fi

email_test_api_password=$(kubectl get --ignore-not-found secret -n "${DEPLOY_NAMESPACE}" maildev-web -o jsonpath="{.data.web-password}" | base64 -d)

# TODO: This is a workaround to mitigate the current secret handling
the_usual_portal_central_navigation_secret=$(kubectl get --ignore-not-found secret -n "${DEPLOY_NAMESPACE}" "${RELEASE_NAME}-portal-server-central-navigation-shared-secret" -o jsonpath="{.data['authenticator\.secret']}" | base64 -d)
the_other_portal_central_navigation_secret=$(kubectl get --ignore-not-found secret -n "${DEPLOY_NAMESPACE}" "${RELEASE_NAME}-opendesk-portal-server-central-navigation" -o jsonpath="{.data['authenticator\.secret']}" | base64 -d)

if [ -n "$the_other_portal_central_navigation_secret" ]
then
    portal_central_navigation_secret="${the_other_portal_central_navigation_secret}"
else
    portal_central_navigation_secret="${the_usual_portal_central_navigation_secret}"
fi

if ! helm list -n "${DEPLOY_NAMESPACE}" | grep -q testing-api; then
echo Installing the testing-api into the namespace
cat <<EOF > values-testing-api.yaml
---
testingApi:
  ldap:
    baseDn: ${ldap_base_dn}
    primaryConnection:
      host: ${RELEASE_NAME}-ldap-server-primary
    secondaryConnection:
      host: ${RELEASE_NAME}-ldap-server-secondary
    auth:
      bindDn:  cn=admin,${ldap_base_dn}
      credentialSecret:
        key: "adminPassword"
        name: ${RELEASE_NAME}-ldap-server-credentials

  ingress:
    host: ${portal_hostname}
...
EOF

helm -n "$DEPLOY_NAMESPACE" upgrade --install --dependency-update testing-api ./helm/testing-api --values values-testing-api.yaml
else
  echo Found a testing-api deployment, skipping install or update.
fi


export PYTEST_ADDOPTS="--portal-base-url=${portal_base_url} --admin-password=${default_admin_password} --portal-central-navigation-secret=${portal_central_navigation_secret} --keycloak-base-url=${keycloak_base_url} --log-level=INFO --email-test-api-username=user --email-test-api-password=${email_test_api_password} --email-test-api-base-url=${email_test_api_base_url}"

echo
echo "Waiting for the creation of the provisioning subscriptions"
kubectl -n "$DEPLOY_NAMESPACE" wait --for=condition=complete jobs.batch "$RELEASE_NAME-provisioning-register-consumers" --timeout 10m

echo
echo "Discovered pytest options: ${PYTEST_ADDOPTS}"
