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
# 2. Source this file to set the environment variables:
#
#        source discover-env-from-cluster.sh
#
# 3. Check the output.


# If no namespace is provided, then try to discover the namespace via "kubectl".
# The parameter "--minify" is important, it ensures that we only get the
# configuration related to the currently selected context.
: "${DEPLOY_NAMESPACE:=$(kubectl config view --minify -o jsonpath='{..namespace}')}"

echo "Namespace: ${DEPLOY_NAMESPACE}"
echo "API Server: $(kubectl config view --minify -o jsonpath='{..server}')"
echo "Cluster: $(kubectl config view --minify -o jsonpath='{.contexts[0].context.cluster}')"


# Discover secrets and the domain.
#
# These commands depend on the Nubus deployment and will have to be kept in sync
# with the progressing Nubus chart.
default_user_password=$(kubectl get secret -n "${DEPLOY_NAMESPACE}" nubus-nubus-credentials -o jsonpath='{.data.user_password}' | base64 -d)
default_admin_password=$(kubectl get secret -n "${DEPLOY_NAMESPACE}" nubus-nubus-credentials -o jsonpath='{.data.admin_password}' | base64 -d)
udm_admin_password=$(kubectl get secret -n "${DEPLOY_NAMESPACE}" nubus-udm-rest-api-credentials -o jsonpath="{.data['machine\.secret']}" | base64 -d)
portal_base_url=https://$(kubectl get ingress -n "${DEPLOY_NAMESPACE}" nubus-portal-server -o jsonpath="{.spec.rules[0].host}")


export PYTEST_ADDOPTS="--portal-base-url=${portal_base_url} --username=default.user --password=${default_user_password} --udm-admin-username='cn=admin' --udm-admin-password=${udm_admin_password} --admin-username=default.admin --admin-password=${default_admin_password}"


echo
echo "Discovered pytest options: ${PYTEST_ADDOPTS}"
