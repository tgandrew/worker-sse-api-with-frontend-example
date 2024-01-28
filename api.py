import asyncio
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from redis import Redis
from rq import Queue
from sse_starlette.sse import EventSourceResponse

from util import status_event_generator
from worker import query as worker_query

logger = logging.getLogger()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

r = Redis(host="my_redis")
q = Queue('my_queue', connection=r)

@app.get('/')
async def index():
    return {'hello': 'world'}


@app.get('/query')
async def query(request: Request, stream: bool = False):
    job = q.enqueue(worker_query, "Test123")
    if stream:
        return await message_stream(job.id)
    else:
        return job.id



@app.get("/stream")
async def message_stream(request_id: str):
    event_generator = status_event_generator(request_id)
    return EventSourceResponse(event_generator)