from threading import Thread
import time


class Component :
    def __init__(self):
        pass

    def update_property(self):
        pass

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
