# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import logging

from tenacity import before_sleep_log, retry, stop_after_delay, wait_fixed

log = logging.getLogger(__name__)

retrying = retry(
    stop=stop_after_delay(20),
    wait=wait_fixed(2),
    before_sleep=before_sleep_log(log, logging.WARNING),
)
"""
A prepared decorator to retry a call with a default configuration.

The decorator is configured to log every retry on level `logging.WARNING`, so
that Pytest does capture the log entries by default and output them for failed
tests.

The intended usage is as follows::

    def test_something(email_test_api)
        retrying(email_test_api.get_one_email)(to=user_recovery_email)

Typically the function ``your_function`` cannot know if and how long it should
retry. E.g. trying to fetch an email may take a few seconds to work out if the
email is generated by a queue asynchronously. It may as well be wrong to retry
if the email is created synchronously and a delay would indicate an issue with
the implementation.

Due to this reason the ``retry`` decorator often cannot reasonably be applied
to a fixture like ``email_test_api`` directly, it depends on the test if
retrying is correct or wrong. This is why the example above is most of the time
the correct way of implementing retry functionality.

Ad-hoc customization of the decorator is possible by using the API's provided
from `tenacity` on the wrapped funtion::

    def test_something(email_test_api)
        get_one_email_retry = retrying(
            email_test_api.get_one_email).retry_with(stop=stop_after_delay(50))
        email = get_one_email_retry(to=user_recovery_email)

Be aware that creating your own instance via ``retry`` is an alternative
option::

    def test_something(email_test_api)
        my_retrying = retry(
            stop=stop_after_delay(60),
            wait=wait_fixed(10),
            before_sleep=before_sleep_log(log, logging.WARNING),
        )
        my_retrying(email_test_api.get_one_email)(to=user_recovery_email)

See: https://tenacity.readthedocs.io/en/latest/
"""


retrying_slow = retry(
    stop=stop_after_delay(40),
    wait=wait_fixed(6),
    before_sleep=before_sleep_log(log, logging.WARNING),
)
