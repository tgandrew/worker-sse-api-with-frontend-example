import asyncio
import time

from redis.asyncio import Redis

r = Redis(host="my_redis", decode_responses=True)

async def status_event_generator(request_id):
    last_id = '0'
    last_time = time.time()
    looping = True
    while looping:
        print('here')
        messages = await r.xread({request_id: last_id})

        if (time.time() - last_time) > 60:
            looping = False
            yield {
                "event": "timeout",
                "data" : "test"
            }
            break
        
        for stream_id, data in messages:
            for msg_id, packet in data:               
                if packet['msg'] == "STOP":
                    looping = False
                    yield {
                        "event": "end",
                        "data" : "test"
                    }
                    break

                print(f"Received message {packet} with ID {msg_id} from {stream_id}")
                yield {
                    "event": "update",
                    "retry": 1000,
                    "data": packet['msg']
                } 
                last_id = msg_id
                last_time = time.time()

        await asyncio.sleep(1)
