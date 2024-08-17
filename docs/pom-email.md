# Page Object Model for Email

Some of the tests cover email related functionality, e.g. the password forgotten
flow. The concept of the "Page Object Model" is roughly applied to create an
abstraction for emails as well. This file describes the design considerations.


## Overview of involved parties

- `email_test_api` is a pytest fixture which should be the main entry point when
  testing emails. It does provide an API to find emails, currently the only
  implementation is for the Maildev API.

- `api.maildev.MaildevApi` provides an API to find emails in the stub email
  server used for testing.

- `api.maildev.MaildevEmail` provides an API to query an individual email which
  has been found via `MaildevApi`. It allows access to attributes like the email
  text.

- `e2e.email.password_reset.PasswordResetEmail` follows the idea of a "Page
  Object Model" but for a specific type of email.


## Retrying

Sending emails is often triggered via a queue in between and as such
asynchronous. This does lead to a common scenario where a test has to "wait"
until an email has been sent.

The library [Tenacity][tenacity-docs] has been included for this purpose
together with the decorator `e2e.decorators.retrying` to simplify the usage of
Tenacity.

[tenacity-docs]: https://tenacity.readthedocs.io/en/latest/


## Waiting

Waiting is discouraged, there is no reasonable way to define how fast a
deployment is expected to be. Instead a solution based on retrying until a
reasonable timeout should be used, this is also closer to what a user would do
when trying to find out if an email is already there.

Waiting would mean to use the timeout which one would use in a retry
configuration and always wait for the longest reasonable amount of time. This
would make the test suite unnecessary slow.
