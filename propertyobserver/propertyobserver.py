import threading
import json
from enum import Enum


class PropertyObserver(threading.Thread):
    def __init__(self, feature_property, observer, runner=None):
        self.feature_property = feature_property
        self.runner = runner
        self.observe = observer
        self.stop_event = threading.Event()
        super(PropertyObserver, self).__init__()

    # def observe(self):
    #   return

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
    @staticmethod
    def execute(self, file_path):
        print("file_observer!")
        with open(file_path, 'r') as fp:
            return json.load(fp)


class FunObserver:
    @staticmethod
    def execute(self, test):
        print("HAHAHAHA")
        print(test)
        return test


class Observer(Enum):
    FILE = FileObserver
    FUN = FunObserver

