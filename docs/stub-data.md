# Stub data

## Guiding principles

1. It MUST BE possible to repeat a test run with the same data.

## Randomized data

Using randomized data is fine, there MUST BE a way though to repeat a run with
the same seed.

The Faker fixtures are automatically seeded by the Pytest integration so that
the generated values are stable.
