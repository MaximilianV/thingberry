from .propertyobserver import PropertyObserver
from time import sleep


class PermanentObserver(PropertyObserver):
    def __init__(self, *args, **kwargs):
        super(PermanentObserver, self).__init__(*args, **kwargs)

    def run(self):
        running = True
        while running:
            self.notify(self.observe(self.config))
            if self.stopped():
                print("stop")
                running = False
