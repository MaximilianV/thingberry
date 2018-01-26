from component import Component
from threading import Thread


class ActionComponent(Component):
    def start_action(self, config):
        thread = Thread(target=self.trigger_action, kwargs=config)
        thread.daemon = True
        thread.start()

    def trigger_action(self, action_name, action_config):
        pass
