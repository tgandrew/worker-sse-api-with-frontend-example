import asyncio
import logging

from redis.asyncio import Redis

r = Redis(host="my_redis")

logger = logging.getLogger()

status_stream_delay = 5  # second
status_stream_retry_timeout = 30000  # milisecond


async def status_event_generator(id):
    async with r.pubsub() as pubsub:
        await pubsub.subscribe(id)
        while True:
            message = await pubsub.get_message(ignore_subscribe_messages=True)
            if message is not None:
                msg = message['data']
                if msg == "STOP":
                    yield {
                        "event": "end",
                        "data" : "test"
                    }
                    break
                yield {
                    "event": "update",
                    "retry": status_stream_retry_timeout,
                    "data": msg
                } 
