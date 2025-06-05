# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

from typing import Any

from e2e.helm import add_release_prefix
from e2e.kubernetes import KubernetesCluster


class UCR:
    def __init__(self, k8s: KubernetesCluster, release_name: str) -> None:
        self.k8s = k8s
        self.release_name = release_name
        self.configmap_name = add_release_prefix("stack-data-ums-ucr", release_name)
        self.configmap = k8s.get_configmap(self.configmap_name)
        self.vars = self._config_map_str_to_vars(self.configmap.data["base.conf"])

    def _config_map_str_to_vars(self, configmap: str) -> dict[str, Any]:
        vars = configmap.split("\n")
        res = {}
        for var in vars:
            if not var:
                continue

            try:
                key, value = var.split(":", 1)
                key = key.strip()
                value = value.lstrip()

                res[key] = value
            except ValueError:
                print(f'failed to process var: "{var}"')
                continue

        return res

    def _vars_to_config_map_str(self):
        res = ""
        for key, value in self.vars.items():
            res += f"{key}: {value}\n"
        return res

    def get(self, key: str) -> str:
        return self.vars[key]

    def get_int(self, key: str) -> int:
        return int(self.get(key))

    def set(self, key, value):
        self.vars[key] = value
        self._save()

    def _save(self):
        self.k8s.update_configmap_data("base.conf", self._vars_to_config_map_str(), self.configmap_name)
