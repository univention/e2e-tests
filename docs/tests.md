# Test Cases

Guideline and hints regarding the implementation of test cases.


## Multiple assertions

Ideally a test case should check one thing and be structured as follows:

1. Prepare
2. Take action
3. Check result

Having multiple asserts potentially mixed up with interim steps does mean that a
failing assertion will hide the state of all following ones.

The following strategies should be applied to improve the situation.


### Split if reasonably possible

If *reasonably* possible, then split the test case into two tests or more tests.

Consider the usage of Pytest's fixtures to prepare once and use the result in
multiple test cases.

Consider the usage of a class to group related cases together.


### Use the `subtests` fixture

The `subtests` fixture allows to capture multiple states in a test case. It can
be used as a decorator:

```python
def test_example(subtests):

    with subtests.test(msg="First check will fail"):
        assert False

    with subtests.test(msg="First check will pass"):
        assert True
```
