from thingconnector.thingconnector import ThingConnector
import logging


class Component:
    def __init__(self, thing_id, **kwargs):
        self.thing_id = thing_id
        self.connector = ThingConnector()
