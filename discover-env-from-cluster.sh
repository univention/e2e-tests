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
default_user_password=$(kubectl get secret -n "${DEPLOY_NAMESPACE}" "${RELEASE_NAME}-nubus-credentials" -o jsonpath="{.data.user_password}" | base64 -d)
default_admin_password=$(kubectl get secret -n "${DEPLOY_NAMESPACE}" "${RELEASE_NAME}-nubus-credentials" -o jsonpath="{.data.admin_password}" | base64 -d)
udm_admin_password=$(kubectl get secret -n "${DEPLOY_NAMESPACE}" "${RELEASE_NAME}-udm-rest-api-credentials" -o jsonpath="{.data['machine\.secret']}" | base64 -d)
portal_base_url=https://$(kubectl get ingress -n "${DEPLOY_NAMESPACE}" "${RELEASE_NAME}-portal-server" -o jsonpath="{.spec.rules[0].host}")
keycloak_base_url=https://$(kubectl get ingress -n "${DEPLOY_NAMESPACE}" "${RELEASE_NAME}-keycloak-extensions-proxy" -o jsonpath="{.spec.rules[0].host}")
email_test_api_base_url=https://$(kubectl get ingress -n "${DEPLOY_NAMESPACE}" maildev -o jsonpath="{.spec.rules[0].host}")
email_test_api_password=$(kubectl get secret -n "${DEPLOY_NAMESPACE}" maildev-web -o jsonpath="{.data.web-password}" | base64 -d)

# TODO: This is a workaround to mitigate the current secret handling
the_usual_portal_central_navigation_secret=$(kubectl get secret -n "${DEPLOY_NAMESPACE}" "${RELEASE_NAME}-portal-server-central-navigation-shared-secret" -o jsonpath="{.data['authenticator\.secret']}" | base64 -d)
the_other_portal_central_navigation_secret=$(kubectl get secret -n "${DEPLOY_NAMESPACE}" "${RELEASE_NAME}-opendesk-portal-server-central-navigation" -o jsonpath="{.data['authenticator\.secret']}" | base64 -d)

if [ -n "$the_other_portal_central_navigation_secret" ]
then
    portal_central_navigation_secret="${the_other_portal_central_navigation_secret}"
else
    portal_central_navigation_secret="${the_usual_portal_central_navigation_secret}"
fi

export PYTEST_ADDOPTS="--portal-base-url=${portal_base_url} --username=default.user --password=${default_user_password} --udm-admin-username='cn=admin' --udm-admin-password=${udm_admin_password} --admin-username=default.admin --admin-password=${default_admin_password} --email-test-api-username=user --email-test-api-password=${email_test_api_password} --email-test-api-base-url=${email_test_api_base_url} --portal-central-navigation-secret=${portal_central_navigation_secret} --keycloak-base-url=${keycloak_base_url}"


echo
echo "Discovered pytest options: ${PYTEST_ADDOPTS}"
