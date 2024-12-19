# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH


class ProvisioningApi:
    """
    Represents a deployment of the Provisioning API.
    """

    service_port = 80

    def __init__(self, release_name):
        self.release_name = release_name
        self.service_name = self._apply_release_prefix("provisioning-api")

    def _apply_release_prefix(self, name):
        if not self.release_name or self.release_name == name:
            return name
        return f"{self.release_name}-{name}"
