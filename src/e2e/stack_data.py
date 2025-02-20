# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from base64 import b64decode

import yaml

from e2e.base import BaseDeployment


class StackDataDeployment(BaseDeployment):
    """
    Represents a deployment of stack-data.
    """

    template_context_secret_base_name = "stack-data-ums-context"
    template_context_file_name = "context.yaml"

    def _discover_from_cluster(self):
        template_context_name = self.add_release_prefix(self.template_context_secret_base_name)
        secret = self._k8s.get_secret(template_context_name)
        template_context_yaml = b64decode(secret.data[self.template_context_file_name]).decode()
        self.template_context = yaml.safe_load(template_context_yaml)
