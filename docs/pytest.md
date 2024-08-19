# Pytest recommendations

## Hints for debugging and development

### Display logs

Pytest allows to display the logs during a test run. This can be very useful
when trying to understand what happens during a test case:

```
pytest --cli-log-level=DEBUG
```

This will include the logging output of libraries which e.g. make connections
over the network.

### Trigger `pdb`

When working with the test suite it is often useful to have a "headed" session
stopped and then interact with the Python interpreter. We have `pdbpp` available
in the test suite and Pytest has builtin support for it.

Augment your Python code with on the of two options below:

```pyton
def interesting_function():
    # The lazy way, Pytest will drop you into a debugger
    assert False

    # Trigger the debugger directly
    import pdb; pdb.set_trace()
```

Then run Pytest with headed mode and also with the debugger enabled:

```sh
pytest --headed --pdb
```
