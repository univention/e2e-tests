# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import contextlib
import logging
import queue
import time

import pytest
from kubernetes import client, watch
from kubernetes.client.exceptions import ApiException
from ldap3 import MODIFY_REPLACE

from e2e.helm import add_release_prefix
from e2e.provisioning import ProvisioningApi
from e2e.util import StoppableAsyncThread, wait_until
from univention.provisioning.consumer.api import (
    ProvisioningConsumerClient,
    ProvisioningConsumerClientSettings,
    RealmTopic,
)
from univention.provisioning.models.message import MessageProcessingStatus

log = logging.getLogger(__name__)


async def users_consumer(messages: queue.Queue, api_url: str, username: str, password: str):
    realms_topics = [RealmTopic(realm="udm", topic="users/user")]
    subscription_name = "test-suite-client"

    admin_settings = ProvisioningConsumerClientSettings(
        provisioning_api_base_url=api_url,
        provisioning_api_username=username,
        provisioning_api_password=password,
        log_level="DEBUG",
    )
    admin_client = ProvisioningConsumerClient(admin_settings)
    subscription_password = "stub_password"

    async with admin_client:
        with contextlib.suppress(Exception):
            await admin_client.cancel_subscription(name=subscription_name)
        await admin_client.create_subscription(
            name=subscription_name, password=subscription_password, realms_topics=realms_topics, request_prefill=False
        )

    settings = ProvisioningConsumerClientSettings(
        provisioning_api_base_url=api_url,
        provisioning_api_username=subscription_name,
        provisioning_api_password=subscription_password,
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
                await client.set_message_status(subscription_name, response.sequence_number, MessageProcessingStatus.ok)
                messages.put(response, timeout=1)


@pytest.fixture(scope="session")
def provisioning_api(k8s, release_name):
    return ProvisioningApi(k8s, release_name)


@pytest.fixture
def consumer(k8s, provisioning_api: ProvisioningApi):
    host, port = k8s.port_forward_if_needed(
        target_name=provisioning_api.service_name,
        target_port=provisioning_api.service_port,
        target_type="service",
    )
    messages = queue.Queue()
    consumer_thread = StoppableAsyncThread(
        atarget=users_consumer(
            messages,
            api_url=f"http://{host}:{port}",
            username=provisioning_api.admin_username,
            password=provisioning_api.admin_password,
        ),
    )
    consumer_thread.start()

    # Wait until consumer is set up
    time.sleep(5)

    yield messages
    consumer_thread.stop()
    consumer_thread.join()


def test_provisioning_messages_are_consumed(faker, k8s_chaos, k8s, ldap, consumer, release_name):
    k8s_chaos.pod_kill(label_selectors=ldap.LABELS_ACTIVE_PRIMARY_LDAP_SERVER)
    wait_until(ldap.all_primaries_reachable, False, timeout=k8s.POD_REMOVED_TIMEOUT)
    wait_until(ldap.all_primaries_reachable, True, timeout=k8s.LDAP_READY_TIMEOUT)

    primary = ldap.get_server_for_primary_service()
    conn = primary.connect()
    new_description = change_user_description(faker, conn, ldap.administrator_dn)

    # TODO: Nubus is inconsistent with the nameOverride for this component,
    # using the fallback name interim.
    listener_pod_name = add_release_prefix("provisioning-udm-listener-0", release_name)
    listener_pod_fallback_name = add_release_prefix("provisioning-listener-0", release_name)
    try:
        wait_until_udm_listener_processed_change(ldap.administrator_dn, k8s.namespace, listener_pod_name)
    except ApiException:
        wait_until_udm_listener_processed_change(ldap.administrator_dn, k8s.namespace, listener_pod_fallback_name)

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

    assert msg_changed.body.old["dn"] == ldap.administrator_dn
    assert msg_changed.body.old["properties"]["description"] != new_description
    assert msg_changed.body.new["dn"] == ldap.administrator_dn
    assert msg_changed.body.new["properties"]["description"] == new_description


def change_user_description(faker, conn, user_dn):
    new_description = faker.paragraph()
    with conn:
        conn.modify(user_dn, {"description": [MODIFY_REPLACE, [new_description]]})

    return new_description


def wait_until_udm_listener_processed_change(user_dn, namespace, pod_name):
    # The udm-listener will sometimes crash and need time to start again.
    # Checking the container status is not good enough, because it may start in
    # a state where the ldap-server and/or ldap-notifier are not yet reachable.
    # In this case it will try to re-connect with an internal back-off time.
    log.info("Waiting until the udm-listener got the ldap update.")
    wait_until_pod_log_contains(
        pod_name=pod_name,
        namespace=namespace,
        expected_fragment=f"ldap_listener: [ modify ] dn: '{user_dn}'",
    )


def wait_until_pod_log_contains(pod_name, namespace, expected_fragment, timeout=120):
    v1 = client.CoreV1Api()
    w = watch.Watch()
    stream = w.stream(
        v1.read_namespaced_pod_log,
        name=pod_name,
        namespace=namespace,
        follow=True,
        since_seconds=10,
        _request_timeout=timeout,
    )
    for line in stream:
        log.debug("%s output: %s", pod_name, line)
        if expected_fragment in line:
            break
    else:
        raise Exception("Waiting for listener timed out.")
