import settings
import asyncio
import websockets
import logging
import json


class ThingWatcher:
    def __init__(self, thing):
        self.thing = thing
        self.logger = logging.getLogger(__name__)

    def start_watching(self):
        asyncio.get_event_loop().run_until_complete(self.watch())

    async def watch(self):
        async with websockets.connect('wss://things.apps.bosch-iot-cloud.com/ws/2',
                                      extra_headers=[('Authorization', settings.basic_auth),
                                                     ('x-cr-api-token', settings.api_token),
                                                     ('content-type', 'application/vnd.eclipse.ditto+json')]) as websocket:
            await websocket.send("START-SEND-EVENTS")
            self.logger.info("Requested to start sending events.")
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
        a tuple (path, value) is returned, else None. Exemplary path: 'feature/feat1/properties/prop1/value'.
        :param message: a string containing the received event
        :return: (path, value) or None
        """
        if message == "START-SEND-EVENTS:ACK":
            self.logger.info("INFO: Established connection.")
            return None
        try:
            event_data = json.loads(message)
            topic_elements = event_data["topic"].split("/")
            if topic_elements[0] != self.thing.namespace or topic_elements[1] != self.thing.name:
                self.logger.debug("Message not relevant for this thing.")
                return None
            self.logger.info("Thing updated: changed {} to {}".format(event_data["path"], event_data["value"]))
            return event_data["path"], event_data["value"]
        except json.JSONDecodeError as e:
            self.logger.warning("ERROR: {}".format(e.msg))
            return None
