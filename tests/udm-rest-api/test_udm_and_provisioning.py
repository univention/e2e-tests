# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2025 Univention GmbH

import asyncio
import contextlib

import pytest
import requests
from aiohttp.client_exceptions import ServerDisconnectedError

from e2e.provisioning import ProvisioningApi
from univention.admin.rest.client import UDM
from univention.provisioning.consumer.api import (
    MessageHandler,
    MessageHandlerSettings,
    ProvisioningConsumerClient,
    ProvisioningConsumerClientSettings,
    RealmTopic,
)
from univention.provisioning.models.message import Message


@pytest.fixture(scope="session")
def provisioning_api(k8s_supporting_port_forward, release_name):
    return ProvisioningApi(k8s_supporting_port_forward, release_name)


@pytest.fixture
def create_consumer_task(k8s_supporting_port_forward, provisioning_api: ProvisioningApi):
    host, port = k8s_supporting_port_forward.port_forward_if_needed(
        target_name=provisioning_api.service_name,
        target_port=provisioning_api.service_port,
        target_type="service",
    )

    async def task(api_url: str, username: str, password: str, message_handler_callback):
        try:
            realms_topics = [RealmTopic(realm="udm", topic="users/user")]
            subscription_name = "test-suite-client"

            admin_settings = ProvisioningConsumerClientSettings(
                provisioning_api_base_url=api_url,
                provisioning_api_username=username,
                provisioning_api_password=password,
                log_level="DEBUG",
            )

            subscription_password = "stub_password"
            async with ProvisioningConsumerClient(admin_settings) as admin_client:
                try:
                    await admin_client.create_subscription(
                        name=subscription_name,
                        password=subscription_password,
                        realms_topics=realms_topics,
                        request_prefill=False,
                    )

                    settings = ProvisioningConsumerClientSettings(
                        provisioning_api_base_url=api_url,
                        provisioning_api_username=subscription_name,
                        provisioning_api_password=subscription_password,
                        log_level="DEBUG",
                    )
                    message_handler_settings = MessageHandlerSettings(max_acknowledgement_retries=5)
                    while True:
                        try:
                            async with ProvisioningConsumerClient(settings) as client:
                                print("Wait for messages")
                                await MessageHandler(
                                    client,
                                    [message_handler_callback],
                                    message_handler_settings,
                                ).run()
                        except ServerDisconnectedError:
                            print("Disconnected from server, will retry in 5s")
                            await asyncio.sleep(5)
                finally:
                    print("Delete subscription")
                    await admin_client.cancel_subscription(subscription_name)
        except asyncio.CancelledError:
            print("Consumer task canceled")

    def create_task(message_handler_callback):
        return asyncio.create_task(
            task(
                f"http://{host}:{port}",
                provisioning_api.admin_username,
                provisioning_api.admin_password,
                message_handler_callback,
            )
        )

    return create_task


@pytest.mark.asyncio
@pytest.mark.acceptance_environment
async def test_provisioning_new_extended_attribute(create_consumer_task, auth_token, udm_rest_api):
    received_users = []

    async def provisioning_message_handler(message: Message):
        if message.body.new and not message.body.old:
            received_users.append(message.body.new["dn"])
            assert "testAttribute1" not in message.body.new["properties"]
        elif message.body.new and message.body.old:
            received_users.append(message.body.new["dn"])
            assert (
                "testAttribute1" not in message.body.old["properties"]
                and "testAttribute1" in message.body.new["properties"]
                and message.body.new["properties"]["testAttribute1"] == message.body.new["dn"]
            )

    consumer_task = create_consumer_task(provisioning_message_handler)

    # Wait for subscription to be active
    await asyncio.sleep(5)
    extended_attributes = []
    created_users = []
    changd_users = []

    try:
        udm = UDM.bearer(udm_rest_api.base_url, auth_token)

        module = udm.get("users/user")
        for x in range(5):
            name = f"test-{len(created_users) + 1}"
            print(f"Create user: {name}")
            properties = {
                "username": name,
                "firstname": "John",
                "lastname": "Doe",
                "password": "password",
                "pwdChangeNextLogin": True,
            }
            udm_obj = module.new()
            udm_obj.properties.update(properties)
            udm_obj.save()

            created_users.append(udm_obj.dn)

        time_waited = 0
        while created_users != received_users:
            assert time_waited <= 30, "Timeout waiting for create user provisioning message"
            await asyncio.sleep(1)
            if consumer_task.done() and consumer_task.exception():
                raise consumer_task.exception()
            time_waited += 1

        received_users.clear()

        module = udm.get("settings/extended_attribute")

        udm_obj = module.new(position=f"cn=custom attributes,cn=univention,{udm.get_ldap_base()}")
        udm_obj.properties["name"] = "TestAttribute1"
        udm_obj.properties["CLIName"] = "testAttribute1"
        udm_obj.properties["module"] = ["users/user"]
        udm_obj.properties["default"] = ""
        udm_obj.properties["ldapMapping"] = "univentionFreeAttribute1"
        udm_obj.properties["objectClass"] = "univentionFreeAttributes"
        udm_obj.properties["shortDescription"] = "Test attribute"
        udm_obj.properties["multivalue"] = False
        udm_obj.properties["valueRequired"] = False
        udm_obj.properties["mayChange"] = True
        udm_obj.properties["doNotSearch"] = False
        udm_obj.properties["deleteObjectClass"] = False
        udm_obj.properties["overwriteTab"] = False
        udm_obj.properties["fullWidth"] = True

        udm_obj.save()

        extended_attributes.append(udm_obj.dn)

        # Update extended attrobutes to allow setting it
        print("Refreshing cache")
        headers = {"Accept": "application/json", "Authorization": f"Bearer {auth_token}"}
        response = requests.get(
            udm_rest_api.base_url.rstrip("/") + "/users/user/add",
            headers=headers,
        )
        assert response.status_code == 200

        module = udm.get("users/user")
        for user_dn in created_users:
            print(f"Change user: {user_dn}")
            udm_obj = module.get(user_dn)

            udm_obj.properties["testAttribute1"] = user_dn
            udm_obj.save()
            changd_users.append(udm_obj.dn)

        time_waited = 0
        while changd_users != received_users:
            assert time_waited <= 30, "Timeout waiting for create user provisioning message"
            await asyncio.sleep(1)
            if consumer_task.done() and consumer_task.exception():
                raise consumer_task.exception()
            time_waited += 1
    finally:
        print("Deleting extended attributes")
        module = udm.get("settings/extended_attribute")
        for dn in extended_attributes:
            obj = module.get(dn)
            obj.delete()

        print("Delete users")
        mod = udm.get("users/user")
        for dn in created_users:
            obj = mod.get(dn)
            obj.delete()

        consumer_task.cancel()
        with contextlib.suppress(asyncio.CancelledError):
            await asyncio.gather(consumer_task)
