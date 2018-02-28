from threading import Timer
from thing import Thing
from thingconnector import ThingWatcher
import logging


class Run:
    def __init__(self, run_time=60):
        self.run_time = run_time
        self.thing = Thing()
        self.watcher = ThingWatcher(self)
        self.thing.load_settings()
        print("Loaded settings for " + self.thing.name)
        self.observer = self.thing.get_observers()
        self.actions = self.thing.get_actions()
        print("Loaded " + str(len(self.observer)) + " observer and " + str(len(self.actions)) + " action(s).")
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(relativeCreated)6d %(threadName)s] [%(levelname)-5.5s]  %(message)s",
            handlers=[
                logging.FileHandler("{0}/{1}.log".format("logs", "execution")),
                logging.StreamHandler()
            ])

    def run(self):
        print("Starting observers.")
        self.start_observers()
        print("Starting websocket to listen for changes.")
        self.start_event_websocket()

    def start_observers(self):
        for observer_name, observer_object in self.observer.items():
            print("Starting " + observer_name + " observer in background.")
            observer_object.start_observe()

    def start_event_websocket(self):
        print("Starting websocket")
        self.watcher.start_watching()

    def handle_change(self, event_data):
        topic_elements = event_data["topic"].split("/")
        if topic_elements[0] != self.thing.namespace or topic_elements[1] != self.thing.name:
            logging.info("Message not relevant for this thing.")
            return

        path = event_data["path"]
        value = event_data["value"]
        logging.info("Thing updated: changed {} to {}".format(path, value))
        path_parts = path.split("/")
        if len(path_parts) < 4:
            logging.info("Discarding unimportant update on " + path)
            return
        if path_parts[1] == "features" and path_parts[2] == "actions":
            # a change on an action occured
            if value.lower() != "false":
                self.run_action(path_parts[4], value)

    def run_action(self, action_name, value):
        self.actions[action_name].start_action(value=value)

    def save_thing(self):
        self.thing.write_settings()


test = Run()
test.run()
