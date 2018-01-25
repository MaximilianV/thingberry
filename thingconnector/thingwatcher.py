import thingconnector.settings as settings
import asyncio
import websockets
import logging
import json


class ThingWatcher:
    def __init__(self, thing):
        self.thing = thing
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(levelname)-5.5s]  %(message)s",
            handlers=[
                logging.StreamHandler()])


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
        the handle_change method is invoked. Exemplary path: 'feature/feat1/properties/prop1/value'.
        :param message: a string containing the received event
        :return: (path, value) or None
        """
        if message == "START-SEND-EVENTS:ACK":
            self.logger.info("INFO: Established connection.")
            return
        try:
            event_data = json.loads(message)
            topic_elements = event_data["topic"].split("/")
            if topic_elements[0] != self.thing.namespace or topic_elements[1] != self.thing.name:
                self.logger.debug("Message not relevant for this thing.")
                return
            self.logger.info("Thing updated: changed {} to {}".format(event_data["path"], event_data["value"]))
            self.handle_change(event_data["path"], event_data["value"])
        except json.JSONDecodeError as e:
            self.logger.warning("ERROR: {}".format(e.msg))

    def handle_change(self, path, value):
        path_parts = path.split("/")
        if len(path_parts) < 4:
            self.logger.debug("Discarding unimportant update on " + path)
            return
        self.logger.debug(path_parts)
        if path_parts[1] == "features" and path_parts[2] == "actions":
            # a change on an action occured
            if value.lower() != "false":
                self.thing.trigger_action(path_parts[4], value)
