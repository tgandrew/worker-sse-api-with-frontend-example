# worker-sse-api-with-frontend-example

An example project for handling long running tasks while sending status info to the user

- Redis PubSub
- RQ Worker
- Fast API
- Starlette SSE

## TODO

- Figure out race condition of redirect from query to stream endpoing which causes client to miss the first message from the worker
- Figure out why running without hardcoded sleeps causes no pubsub comms