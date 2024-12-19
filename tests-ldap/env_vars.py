# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

# env_vars.py
import base64

from kubernetes import client, config


class EnvConfig:
    def __init__(self, namespace, release_name):
        self.k8s_namespace = namespace
        self.release_name = release_name
        if self.release_name:
            self.release_prefix = f"{self.release_name}-"
        else:
            self.release_prefix = ""

        self.k8s_api = client.CoreV1Api()

        # Load configurations from ConfigMap and Secret
        self._load_configs()

    def _load_configs(self):
        try:
            # Get ConfigMap
            config_map = self.k8s_api.read_namespaced_config_map(
                name=f"{self.release_prefix}ldap-server",
                namespace=self.k8s_namespace,
            )

            # Get Secret
            secret = self.k8s_api.read_namespaced_secret(
                name=f"{self.release_prefix}ldap-server-credentials",
                namespace=self.k8s_namespace,
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

        except client.rest.ApiException as e:
            raise RuntimeError(f"Failed to load Kubernetes configurations: {e}")
        except KeyError as e:
            raise RuntimeError(f"Missing required configuration key: {e}")
