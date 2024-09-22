# SPDX-License-Identifier: AGPL-3.0-only
# SPDX-FileCopyrightText: 2024 Univention GmbH

import asyncio
import logging
from contextlib import asynccontextmanager

import nats

from testing_api.config import TestingApiSettings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def jetstream_connection(settings: TestingApiSettings):
    async with await nats.connect(
        servers=settings.nats_server, user=settings.nats_user, password=settings.nats_password, max_reconnect_attempts=1
    ) as nc:
        js = nc.jetstream()
        yield js


async def subscription_status(settings: TestingApiSettings, name: str):
    async with jetstream_connection(settings) as js:
        stream_info = await js.stream_info(stream_name(name))

    result = {"pending_messages": stream_info.state.messages, "last_sequence_number": stream_info.state.last_seq}
    logger.debug("Stream info for stream: %s is: %r", name, result)
    return result


async def check_subscription_status(
    settings: TestingApiSettings, name: str, sequence_number: int, debounce: float | int
) -> None:
    async with jetstream_connection(settings) as js:
        last_sequence_number = 0
        stable_time_start = None

        while True:
            stream_info = await js.stream_info(stream_name(name))
            current_sequence_number = stream_info.state.last_seq
            if current_sequence_number != last_sequence_number or stream_info.state.messages > 0:
                last_sequence_number = current_sequence_number
                stable_time_start = None
            elif stable_time_start is None:
                stable_time_start = asyncio.get_event_loop().time()
            elif all(
                (
                    current_sequence_number > sequence_number,
                    asyncio.get_event_loop().time() - stable_time_start >= debounce,
                )
            ):
                return
            await asyncio.sleep(0.25)


def stream_name(subscription: str) -> str:
    return f"stream:{subscription}"
