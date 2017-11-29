from .propertyobserver import PropertyObserver
from time import sleep


class IntervalObserver(PropertyObserver):
    def __init__(self, interval=1000, *args, **kwargs):
        self.interval = interval
        super(IntervalObserver, self).__init__(*args, **kwargs)

    def run(self):
        running = True
        while running:
            self.notify(self.observe("wtf"))
            sleep(self.interval / 1000)
            if self.stopped():
                print("stop")
                running = False
