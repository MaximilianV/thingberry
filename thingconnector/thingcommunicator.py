import thingconnector.settings as settings
import json
import websockets
import asyncio


class ThingCommunicator:

    async def hello():
        async with websockets.connect('wss://things.apps.bosch-iot-cloud.com/ws/2',
                                      extra_headers=[('Authorization', settings.basic_auth),
                                                     ('x-cr-api-token', settings.api_token),
                                                     ('content-type',
                                                      'application/vnd.eclipse.ditto+json')]) as websocket:
            name = json.dumps({"topic": settings.namespace + "/thingberry/things/twin/commands/modify",
                               "headers": {"correlation-id": "a780b7b5-fdd2-4864-91fc-80df6bb0a636",
                                           "response-required": True},
                               "path": "/features/camera/properties/lastTriggered",
                               "value": "123test123098"
                               })
            # name = "START-SEND-EVENTS"
            """name = json.dumps({"topic": "hpi.test/wstest2/things/twin/commands/create",
                       "headers": {"correlation-id": "a780b7b5-fdd2-4864-91fc-80df6bb0a636", "response-required": True},
                       "path": "/",
                       "value": {

                               "thingId": "hpi.test:wstest2",
                               "attributes": {},
                               "features": {
                                   "feat1": {
                                       "properties": {
                                           "prop11": {
                                               "value": "abc"
                                           }
                                       }
                                   }
                               }

                       }})"""

            """
            name = "START-SEND-EVENTS
            """

            await websocket.send(name)
            print("> {}".format(name))

            greeting = await websocket.recv()
            print("< {}".format(greeting))

            greeting = await websocket.recv()
            print("< {}".format(greeting))

    asyncio.get_event_loop().run_until_complete(hello())