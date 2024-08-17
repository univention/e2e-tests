# Pytest recommendations

## Hints for debugging

### Display logs

Pytest allows to display the logs during a test run. This can be very useful
when trying to understand what happens during a test case:

```
pytest --cli-log-level=DEBUG
```

This will include the logging output of libraries which e.g. make connections
over the network.
