import asyncio
import contextlib
import logging
import threading
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


class StoppableAsyncThread(threading.Thread):
    """
    Utility to run async code in a thread in the background.

    Either override the method `arun` with your own implementation or
    provide the keyword argument `atarget`.

    The method `stop` will raise a `CancelledError` in the running `atarget`.
    """

    def __init__(self, *, atarget=None):
        super().__init__()
        self._atarget = atarget
        self._should_stop = threading.Event()

    def run(self):
        asyncio.run(self._run_arun_until_stopped())

    async def _run_arun_until_stopped(self):
        task_atarget = asyncio.create_task(self.arun())

        while not self.stopped():
            await asyncio.sleep(0.1)

        task_atarget.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await task_atarget

    async def arun(self):
        if not self._atarget:
            return
        await self._atarget

    def stop(self):
        self._should_stop.set()

    def stopped(self):
        return self._should_stop.is_set()
