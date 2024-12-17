import logging
import time


log = logging.getLogger(__name__)


def wait_until(func, expected, timeout=10):
    for _ in range(timeout):
        if func() == expected:
            break
        log.debug("Waiting until %s is %s", func, expected)
        time.sleep(1)
    else:
        raise Exception("Timed out in wait_until.")
