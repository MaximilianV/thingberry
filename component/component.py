from thingconnector.thingconnector import ThingConnector
from datetime import datetime


class Component:
    def __init__(self, thing_id, **kwargs):
        self.thing_id = thing_id
        self.connector = ThingConnector()

    @staticmethod
    def get_timestamp():
        return str(datetime.now())
