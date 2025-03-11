# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import asyncio
import logging
import threading

from e2e.util import StoppableAsyncThread

log = logging.getLogger(__name__)


class PortForwardingManager:
    """
    Utility to manage multiple port-forwarding subprocesses.

    Due to the usage in a context where Pods are intentionally being killed,
    this utility has to ensure that the port-forwardings are re-established
    whenever they terminate. It does run a monitoring thread in the background
    for this purpose to keep an eye on all processes.

    When working on this class, using the following command to observe the
    subprocesses is useful for troubleshooting:

        watch "ps | grep kubectl"

    """

    _worker_thread = None

    def __init__(self, first_local_port=3890):
        self._loop = None
        self._running = threading.Event()
        self._processes = {}
        self._next_local_port = first_local_port

    def add(self, namespace, name, target_port, local_port=None, target_type="pod"):
        process_data = ProcessData(namespace, name, local_port, target_port, target_type, None)
        if not self._loop:
            raise RuntimeError("Forwarding manager has not been started.")
        future = asyncio.run_coroutine_threadsafe(
            self._add(process_data),
            self._loop,
        )
        used_local_port = future.result()
        return used_local_port

    def start_monitoring(self):
        if not self._worker_thread:
            self._worker_thread = StoppableAsyncThread(atarget=self._run())
        self._worker_thread.start()
        self._running.wait(timeout=5)

    def stop_monitoring(self):
        if self._worker_thread:
            self._worker_thread.stop()

    async def _terminate(self):
        log.debug("Terminating all forwarding processes.")
        for process_data in self._processes.values():
            await _terminate_process(process_data.process)
        self._processes.clear()
        log.debug("Stopped all forwarding processes.")

    async def _add(self, process_data):
        if process_data.key() not in self._processes:
            if process_data.local_port is None:
                process_data.local_port = self._next_local_port
                self._next_local_port += 1
            await self._start_new_port_forward(process_data)
            local_port = process_data.local_port
        else:
            existing_data = self._processes[process_data.key()]
            local_port = existing_data.local_port
        return local_port

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

    async def _start_new_port_forward(self, process_data):
        cmd = [
            "kubectl",
            "port-forward",
            f"{process_data.target_type}/{process_data.name}",
            f"{process_data.local_port}:{process_data.target_port}",
            "-n",
            process_data.namespace,
        ]
        log.debug("Starting new forward via kubectl: %s", " ".join(cmd))
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        process_data.process = process
        self._processes[process_data.key()] = process_data
        asyncio.create_task(self._monitor_process(process_data))
        asyncio.create_task(self._log_output(process_data))
        return process

    async def _monitor_process(self, process_data):
        await process_data.process.wait()
        await asyncio.sleep(1)
        if self._running.is_set():
            log.debug("Restarting process: %s", process_data)
            await self._start_new_port_forward(process_data)

    async def _log_output(self, process_data):
        await asyncio.gather(
            self._log_output_stream("stdout", process_data, process_data.process.stdout),
            self._log_output_stream("stderr", process_data, process_data.process.stderr),
        )

    async def _log_output_stream(self, prefix, key, stream):
        async for line in stream:
            content = line.decode()
            log.debug("kubectl %s/%s %s: %s", key.target_type, key.name, prefix, content)


class ProcessData:
    """
    The relevant data regarding one forwarding process.
    """

    def __init__(self, namespace, name, local_port, target_port, target_type, process):
        self.namespace = namespace
        self.name = name
        self.local_port = local_port
        self.target_port = target_port
        self.target_type = target_type
        self.process = process

    def key(self):
        return (self.namespace, self.name, self.target_port, self.target_type)


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
