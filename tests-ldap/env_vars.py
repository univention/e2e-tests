# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

# env_vars.py
import base64
import os

from kubernetes import client, config


class EnvConfig:
    def __init__(self):
        self.k8s_namespace = os.getenv("K8S_NAMESPACE")
        if not self.k8s_namespace:
            raise ValueError("K8S_NAMESPACE environment variable must be set")

        # Initialize Kubernetes client
        config.load_kube_config()
        self.k8s_api = client.CoreV1Api()

        # Load configurations from ConfigMap and Secret
        self._load_configs()

        # Test configurations (hardcoded)
        self.NUM_GROUPS = 10
        self.NUM_USERS = 100
        self.NUM_USERS_TO_MOVE = 50

    def _load_configs(self):
        try:
            # Get ConfigMap
            config_map = self.k8s_api.read_namespaced_config_map(name="nubus-ldap-server", namespace=self.k8s_namespace)

            # Get Secret
            secret = self.k8s_api.read_namespaced_secret(
                name="nubus-ldap-server-credentials", namespace=self.k8s_namespace
            )

            # Set LDAP configurations
            self.LDAP_BASE_DN = config_map.data["LDAP_BASE_DN"]
            self.LDAP_ADMIN_DN = f"cn=admin,{self.LDAP_BASE_DN}"
            self.LDAP_PORT = 8389  # Default LDAP port

            # Decode admin password from base64
            admin_password_b64 = secret.data["adminPassword"]
            self.LDAP_ADMIN_PASSWORD = base64.b64decode(admin_password_b64).decode("utf-8")

            # Additional configurations
            self.DOMAIN_NAME = config_map.data["DOMAIN_NAME"]
            self.LOG_LEVEL = config_map.data["LOG_LEVEL"]
            self.TLS_MODE = config_map.data["TLS_MODE"]

            # Helm-related configurations
            self.HELM_RELEASE_NAME = "nubus"  # Assuming this matches your release name

        except client.rest.ApiException as e:
            raise RuntimeError(f"Failed to load Kubernetes configurations: {e}")
        except KeyError as e:
            raise RuntimeError(f"Missing required configuration key: {e}")


# Create a global instance of the configuration
env = EnvConfig()
