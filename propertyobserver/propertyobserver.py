import threading


class PropertyObserver(threading.Thread):
    def __init__(self, feature_property, runner=None):
        self.feature_property = feature_property
        self.runner = runner
        self.stop_event = threading.Event()
        super(PropertyObserver, self).__init__()

    def observe(self):
        return

    def notify(self, value):
        self.runner.notify(self.feature_property, value)

    def stop(self):
        print("stop event set")
        self.stop_event.set()

    def stopped(self):
        return self.stop_event.is_set()