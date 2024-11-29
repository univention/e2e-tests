# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH


class LDAPFixture:
    # TODO: Remove!
    _stub_context_csn = None

    def __init__(self, user):
        self.user = user

    def get_context_csn(self):
        # TODO: Implement me properly!
        if self._stub_context_csn:
            result = self._stub_context_csn
            self._stub_context_csn = None
            return result

        self.user.reload()
        return self.user.properties["displayName"]

    def inject_changes(self):
        user = self.user
        display_name = user.properties["displayName"]
        for x in range(1, 21):
            user.properties["displayName"] = f"{display_name} - changed {x}"
            user.save()
        latest_display_name = user.properties["displayName"]
        # TODO: Remove!
        self._stub_context_csn = latest_display_name
