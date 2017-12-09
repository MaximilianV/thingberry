import threading
import json
from enum import Enum


class PropertyObserver(threading.Thread):
    def __init__(self, feature_property, observer, config, runner=None):
        self.feature_property = feature_property
        self.observe = observer.value.execute
        self.config = config
        self.stop_event = threading.Event()
        super(PropertyObserver, self).__init__()

    @property
    def runner(self):
        return self._runner

    @runner.setter
    def runner(self, name):
        self._runner = name

    def run(self):
        pass

    def notify(self, value):
        self.runner.notify(self.feature_property, value)

    def stop(self):
        print("stop event set")
        self.stop_event.set()

    def stopped(self):
        return self.stop_event.is_set()


class FileObserver:
    CONFIG_NAME = "file_path"
    CONFIG_SPEAKING_NAME = "file path"

    @staticmethod
    def execute(config):
        print("file_observer!")
        with open(config[FileObserver.CONFIG_NAME], 'r') as fp:
            return json.load(fp)


class PinObserver:
    CONFIG_NAME = "pin"
    CONFIG_SPEAKING_NAME = "input pin"

    @staticmethod
    def execute(config):
        print("pin_observer!")
        channel = GPIO.wait_for_edge(config[PinObserver.CONFIG_NAME], GPIO_RISING, timeout=5000)
        if channel is not None:
            print('Edge detected on channel', channel)
            return "true"


class Observer(Enum):
    FILE = FileObserver
    PIN = PinObserver

