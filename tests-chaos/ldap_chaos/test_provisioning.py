import contextlib
import logging
import queue
import time

from ldap3 import MODIFY_REPLACE
from univention.provisioning.consumer import ProvisioningConsumerClient, ProvisioningConsumerClientSettings
from univention.provisioning.models import RealmTopic, MessageProcessingStatus
import pytest

from e2e.util import StoppableAsyncThread, wait_until


log = logging.getLogger(__name__)

# TODO: Fix duplication.
LABELS_ACTIVE_PRIMARY_LDAP_SERVER = {
    "app.kubernetes.io/name": "ldap-server",
    "ldap-server-type": "primary",
    "ldap-leader": "true",
}


async def users_consumer(messages: queue.Queue):
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


@pytest.fixture
def consumer():
    messages = queue.Queue()
    consumer_thread = StoppableAsyncThread(atarget=users_consumer(messages))
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
