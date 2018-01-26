from component import Component
from threading import Thread


class ActionComponent(Component):
    def __init__(self, action_name, action_config, **kwargs):
        super().__init__(**kwargs)
        self.action_name = action_name
        self.action_config = action_config

    def start_action(self, **kwargs):
        thread = Thread(target=self.trigger_action, kwargs=kwargs)
        thread.daemon = True
        thread.start()

    def trigger_action(self, **kwargs):
        raise NotImplementedError


    @staticmethod
    def configure_action():
        raise NotImplementedError