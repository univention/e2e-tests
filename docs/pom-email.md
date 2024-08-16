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
