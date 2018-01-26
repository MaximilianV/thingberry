from component import Component
from threading import Thread


class ObserverComponent(Component):
    def start_observe(self, config):
        thread = Thread(target=self.observe, kwargs=config)
        thread.daemon = True
        thread.start()

    def observe(self, feature, thing_property, pin):
        while True:
            print("[O] I'm a observer for property " + thing_property + " !")
