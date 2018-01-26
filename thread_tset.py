from threading import Thread
import time


class Component:
    def __init__(self):
        print("A new component was born!")

    def update_thing(self, message):
        print(message)

    def start_observe(self, config):
        thread = Thread(target=self.observe, kwargs=config)
        thread.daemon = True
        thread.start()

    def start_action(self, config):
        thread = Thread(target=self.trigger_action, kwargs=config)
        thread.daemon = True
        thread.start()

    def observe(self, feature, thing_property, pin):
        while True:
            print("[O] I'm a observer for property " + thing_property + " !")
            time.sleep(3)

    def trigger_action(self, action_name, action_config):
        print("[A] Started action " + action_name)
        print("[A] Doing some work")
        self.update_thing("[A] update!")
        time.sleep(2)
        print("[A] More work")
        self.update_thing("[A] update!")
        time.sleep(3)
        print("[A] Finished!")


comp = Component()
print("Now starting observer")
comp.start_observe({"feature": "camera", "thing_property": "prop1", "pin": 11})
print("Now starting action")
comp.start_action({"action_name": "action1", "action_config": {}})
print("Now starting action")
comp.start_action({"action_name": "action2", "action_config": {}})

time.sleep(20)

