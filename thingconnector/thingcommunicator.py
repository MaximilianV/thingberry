import settings
import json
import websockets
import asyncio


async def consumer_handler(websocket):
    async for message in websocket:
        await consumer(message)


async def producer_handler(websocket):
    while True:
        message = await producer()
        await websocket.send(message)


async def handler(websocket):
    while True:
        consumer_task = asyncio.ensure_future(consumer_handler(websocket))
        producer_task = asyncio.ensure_future(producer_handler(websocket))
        done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:
            task.cancel()


ws = websockets.connect('wss://things.apps.bosch-iot-cloud.com/ws/2',
                                  extra_headers=[('Authorization', settings.basic_auth),
                                                 ('x-cr-api-token', settings.api_token),
                                                 ('content-type', 'application/vnd.eclipse.ditto+json')])

await handler(ws)

def consumer(message):
    print(json.loads(message))

def producer():
    return "START-SEND-EVENTS"


class ThingCommunicator:
    WEBSOCKET_URL = "wss://things.apps.bosch-iot-cloud.com/ws/2"

    def get_test_envelope(self):
        return {"topic": "hpi.test/wstest/things/twin/commands/modify",
                "headers": None,
                "path": "/feature/feat1/properties/prop11",
                # "fields": "thingId",
                "value": {"value": "def"}}

    def get_test_payload(self):
        return {"com.friedow:wstest"}