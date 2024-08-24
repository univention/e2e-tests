# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

from operator import attrgetter
from urllib.parse import urljoin

import dateutil.parser


class MaildevApi:
    """
    An abstraction of the API provided by "Maildev".

    See: https://maildev.github.io/maildev/
    """

    def __init__(self, base_url, session):
        self._base_url = base_url
        self._session = session

    def get_one_email(self, *, to=None):
        """
        Searches an email and ensures to return exactly one result.

        Supported filters must be specified as keyword arguments.

        :param to: Allows to filter by the `To` header values in the email.
        """
        email_url = urljoin(self._base_url, "/email")
        response = self._session.get(email_url)
        response.raise_for_status()
        all_emails = response.json()

        found_emails = []
        for email in all_emails:
            if email["to"][0]["address"] == to:
                found_emails.append(MaildevEmail(email))

        if not found_emails:
            raise RuntimeError("No matching email found.")

        found_email = _get_latest_email(found_emails)

        return found_email


def _get_latest_email(emails):
    emails = sorted(emails, key=attrgetter("date"), reverse=True)
    return emails[0]


class MaildevEmail:
    """
    An abstraction of an email and the specific implementation for Maildev.
    """

    def __init__(self, data):
        self._data = data

    @property
    def text(self):
        """
        The plain text variant of the email.
        """
        return self._data["text"]

    @property
    def date(self):
        """
        The datetime based on the email's header "Date".
        """
        return dateutil.parser.isoparse(self._data["date"])
