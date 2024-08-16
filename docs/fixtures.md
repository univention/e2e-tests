# Fixture Design Principles

## Fixtures which connect to APIs

Fixtures which do connect to an API like the UDM Rest API or the Maildev based
email API should verify the correctness of the configuration early on.

This gives fast feedback when using the test suite with incorrect credentials or
missing configuration.

See `email_test_api_session` for an example.
