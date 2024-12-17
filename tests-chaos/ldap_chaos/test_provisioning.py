import asyncio
import contextlib
import logging
import queue
import random
import threading
import time

from ldap3 import MODIFY_REPLACE

from univention.provisioning.consumer import ProvisioningConsumerClient, ProvisioningConsumerClientSettings
from univention.provisioning.models import RealmTopic, MessageProcessingStatus

import pytest


log = logging.getLogger(__name__)

# TODO: Fix duplication.
LABELS_ACTIVE_PRIMARY_LDAP_SERVER = {
    "app.kubernetes.io/name": "ldap-server",
    "ldap-server-type": "primary",
    "ldap-leader": "true",
}


async def stub_consumer(messages: queue.Queue):
    realms_topics = [RealmTopic(realm="udm", topic="users/user")]
    subscription_name = "test-suite-client"

    admin_settings = ProvisioningConsumerClientSettings(
        provisioning_api_base_url="http://localhost:8100",
        provisioning_api_username="admin",
        provisioning_api_password="provisioning",
        log_level="DEBUG",
    )
    admin_client = ProvisioningConsumerClient(admin_settings)

    async with admin_client:
        with contextlib.suppress(Exception):
            await admin_client.cancel_subscription(name=subscription_name)
        await admin_client.create_subscription(
            name=subscription_name,
            password="password",
            realms_topics=realms_topics,
            request_prefill=False)

    settings = ProvisioningConsumerClientSettings(
        provisioning_api_base_url="http://localhost:8100",
        provisioning_api_username=subscription_name,
        provisioning_api_password="password",
        log_level="DEBUG",
    )
    client = ProvisioningConsumerClient(settings)


    async with client:
        while True:
            response = await client.get_subscription_message(
                subscription_name,
                timeout=1,
            )
            if response:
                await client.set_message_status(
                    subscription_name, response.sequence_number, MessageProcessingStatus.ok
                )
                messages.put(response, timeout=1)


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
    messages = queue.Queue()
    consumer_thread = StoppableAsyncThread(atarget=stub_consumer(messages))
    consumer_thread.start()

    # Wait until consumer is set up
    time.sleep(5)

    yield messages
    consumer_thread.stop()
    consumer_thread.join()


def test_provisioning(faker, k8s_chaos, ldap, consumer):
    k8s_chaos.pod_kill(label_selectors=LABELS_ACTIVE_PRIMARY_LDAP_SERVER)
    wait_until(ldap.all_primaries_reachable, False, timeout=5)
    wait_until(ldap.all_primaries_reachable, True, timeout=40)

    primary = ldap.get_server_for_primary_service()
    conn = primary.conn
    user_dn, new_description = change_administrator_description(faker, conn)

    messages = []
    expected_number_of_messages = 1
    timeout = 5
    try:
        while True:
            log.debug("Waiting for a message with a timeout of %s", timeout)
            messages.append(consumer.get(timeout=timeout))
    except queue.Empty:
        log.debug("Consumed queue")

    assert len(messages) == expected_number_of_messages
    msg_changed = messages[0]

    assert msg_changed.body.old["dn"] == user_dn
    assert msg_changed.body.old["properties"]["description"] != new_description
    assert msg_changed.body.new["dn"] == user_dn
    assert msg_changed.body.new["properties"]["description"] == new_description


def change_administrator_description(faker, conn):
    base_dn = "dc=univention-organization,dc=intranet"
    users_container_dn = f"cn=users,{base_dn}"
    user_dn = f"uid=Administrator,{users_container_dn}"

    new_description = faker.paragraph()
    with conn:
        conn.modify(user_dn, {"description": [MODIFY_REPLACE, [new_description]]})

    return user_dn, new_description


# TODO: Fix duplication
def wait_until(func, expected, timeout=10):
    for _ in range(timeout):
        if func() == expected:
            break
        log.debug("Waiting until %s is %s", func, expected)
        time.sleep(1)
    else:
        raise Exception("Timed out in wait_until.")
