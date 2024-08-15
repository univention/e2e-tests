
from urllib.parse import urljoin


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

        for email in all_emails:
            if email["to"][0]["address"] == to:
                return email
        else:
            raise RuntimeError("No matching email found.")
