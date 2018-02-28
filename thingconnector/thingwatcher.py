import thingconnector.settings as settings
import asyncio
import websockets
import logging
import json


class ThingWatcher:
    def __init__(self, runner):
        self.runner = runner

    def start_watching(self):
        asyncio.get_event_loop().run_until_complete(self.watch())

    async def watch(self):
        async with websockets.connect('wss://things.apps.bosch-iot-cloud.com/ws/2',
                                      extra_headers=[('Authorization', settings.basic_auth),
                                                     ('x-cr-api-token', settings.api_token),
                                                     ('content-type', 'application/vnd.eclipse.ditto+json')]) as websocket:
            await websocket.send("START-SEND-EVENTS")
            logging.info("Requested to start sending events.")
            while True:
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=20)
                except asyncio.TimeoutError:
                    try:
                        pong_waiter = await websocket.ping()
                        await asyncio.wait_for(pong_waiter, timeout=10)
                    except asyncio.TimeoutError:
                        break
                else:
                    self.handle_message(message)

    def handle_message(self, message):
        """
        Parses a Bosch Thing Event. In case it is an update event for the current thing,
        the handle_change method is invoked. Exemplary path: 'feature/feat1/properties/prop1/value'.
        :param message: a string containing the received event
        :return: (path, value) or None
        """
        if message == "START-SEND-EVENTS:ACK":
            logging.info("INFO: Established connection.")
            return
        try:
            event_data = json.loads(message)
            self.runner.handle_change(event_data)
        except json.JSONDecodeError as e:
            logging.warning("ERROR: {}".format(e.msg))
