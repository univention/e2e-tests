import asyncio
import contextlib
import threading
import time

import pytest


async def stub_consumer():
    while True:
        print("consume")
        await asyncio.sleep(1)


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


@pytest.fixture
def consumer():
    consumer_thread = StoppableAsyncThread(atarget=stub_consumer())
    consumer_thread.start()
    yield
    consumer_thread.stop()
    consumer_thread.join()


def test_provisioning(faker, ldap, consumer):
    primary = ldap.get_server_for_primary_service()
    conn = primary.conn
    create_and_delete_a_ldap_entry(faker, conn)
    expected_context_csn = [primary.get_context_csn()] * 2
    time.sleep(5)

    # check that consumer did capture an event, with a timeout
    assert False, "finish me!"


# TODO: Duplicated
def create_and_delete_a_ldap_entry(faker, conn):
    base_dn = "dc=univention-organization,dc=intranet"
    users_container_dn = f"cn=users,{base_dn}"

    user_uid = faker.user_name()
    user_dn = f"uid={user_uid},{users_container_dn}"
    user_attributes = {
        "cn": faker.name(),
        "sn": faker.last_name(),
    }

    with conn:
        conn.add(user_dn, "inetOrgPerson", user_attributes)
        conn.delete(user_dn)
