import asyncio
import logging
import threading
import typing

from e2e.util import StoppableAsyncThread


log = logging.getLogger(__name__)


class PortForwardingManager:
    """
    Utility to manage multiple port-forwarding subprocesses.

    Due to the usage in a context where Pods are intentionally being killed,
    this utility has to ensure that the port-forwardings are re-established
    whenever they terminate. It does run a monitoring thread in the background
    for this purpose to keep an eye on all processes.
    """

    def __init__(self):
        self._loop = None
        self._running = threading.Event()
        self._worker_thread = StoppableAsyncThread(atarget=self._run())
        self._processes = {}

    def add(self, namespace, name, local_port, target_port, target_type="pod"):
        if not self._loop:
            raise RuntimeError("Forwarding manager has not been started.")
        future = asyncio.run_coroutine_threadsafe(
            self._add(namespace, name, local_port, target_port, target_type),
            self._loop,
        )
        return future.result()

    def start_monitoring(self):
        self._worker_thread.start()
        self._running.wait(timeout=5)

    def stop_monitoring(self):
        self._worker_thread.stop()

    async def _terminate(self):
        log.debug("Terminating all forwarding processes.")
        for process in self._processes.values():
            await _terminate_process(process)
        self._processes.clear()
        log.debug("Stopped all forwarding processes.")

    async def _add(self, namespace, name, local_port, target_port, target_type):
        key = ProcessKey(namespace, name, local_port, target_port, target_type)
        if not key in self._processes:
            await self._start_new_port_forward(namespace, name, local_port, target_port, target_type)

    async def _run(self):
        try:
            if self._loop is not None:
                raise Exception("Already running.")
            self._running.set()
            self._loop = asyncio.get_running_loop()
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            self.running = False
            await self._terminate()

    async def _start_new_port_forward(self, namespace, name, local_port, target_port, target_type):
        cmd = [
            "kubectl",
            "port-forward",
            f"{target_type}/{name}",
            f"{local_port}:{target_port}",
            "-n",
            namespace,
        ]
        log.debug("Starting new forward via kubectl: %s", " ".join(cmd))
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        key = ProcessKey(namespace, name, local_port, target_port, target_type)
        self._processes[key] = process
        asyncio.create_task(self._monitor_process(key, process))
        asyncio.create_task(self._log_output(key, process))
        return process

    async def _monitor_process(self, key, process):
        await process.wait()
        await asyncio.sleep(1)
        if self._running.is_set():
            log.debug("Restarting process: %s", key)
            await self._start_new_port_forward(
                key.namespace, key.name, key.local_port, key.target_port, key.target_type)

    async def _log_output(self, key, process):
        await asyncio.gather(
            self._log_output_stream("stdout", key, process.stdout),
            self._log_output_stream("stderr", key, process.stderr),
        )

    async def _log_output_stream(self, prefix, key, stream):
        async for line in stream:
            content = line.decode()
            log.debug("kubectl %s/%s %s: %s", key.target_type, key.name, prefix, content)


class ProcessKey(typing.NamedTuple):
    namespace: str
    name: str
    local_port: int
    target_port: int
    target_type: str


async def _terminate_process(process):
    graceful_shutdown_timeout = 5
    if _is_running(process):
        process.terminate()
    try:
        await asyncio.wait_for(process.wait(), timeout=graceful_shutdown_timeout)
    except TimeoutError:
        log.warn("Process did not terminate, trying to kill: %s", process.pid)
        process.kill()


def _is_running(process):
    return process.returncode is None
