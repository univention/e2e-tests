# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import re


class PasswordResetEmail:
    """
    Implements an abstraction over the password reset email.
    """

    def __init__(self, email):
        self._email = email

    @property
    def link_with_token(self):
        email_text = self._email.text
        re_match = re.search(r"^https?://.*?token=.*?$", email_text, flags=re.MULTILINE)
        return re_match.group()
