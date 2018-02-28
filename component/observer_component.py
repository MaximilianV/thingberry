from .component import Component
from threading import Thread
import logging


class ObserverComponent(Component):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.feature_name = None
        self.property_name = None
        self.property_config = None

    def init_observer(self, feature_name, property_name, property_config):
        self.feature_name = feature_name
        self.property_name = property_name
        self.property_config = property_config

    def update_property(self, new_value):
        self.connector.update_property(self.thing_id, self.feature_name, self.property_name, new_value)

    def start_observe(self, **kwargs):
        logging.info("Start observer for " + self.feature_name + "/" + self.property_name)
        thread = Thread(target=self.observe, kwargs=kwargs)
        thread.daemon = True
        thread.start()

    def observe(self, **kwargs):
        raise NotImplementedError

    @staticmethod
    def configure_observer():
        raise NotImplementedError
