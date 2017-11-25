from propertyobserver.file_intervalobserver import FileIntervalObserver
from threading import Timer
from thing import Thing


class Run():
    def __init__(self, run_time=30):
        self.run_time = run_time
        self.thing = Thing()
        self.thing.load_settings()
        print("Loaded settings for " + self.thing.name)
        self.init_observer()

    def init_observer(self):
        thing_features = self.thing.features
        for feature in thing_features:
            for f_property in thing_features[feature]["properties"]:
                self.start((feature, f_property))

    def start(self, f_property):
        fileobs = FileIntervalObserver(f_property[1] + ".json", feature_property=f_property, runner=self)
        fileobs.start()
        t = Timer(self.run_time, fileobs.stop)
        t.start()

    def notify(self, feature_property, value):
        print(feature_property[0] + "/" + feature_property[1] + ":" + str(value))
