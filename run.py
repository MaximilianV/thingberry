from threading import Timer
from thing import Thing


class Run:
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
                observer = self.thing.get_property_observer(f_property, feature)
                observer.runner = self
                observer.start()
                t = Timer(self.run_time, observer.stop)
                t.start()

    def notify(self, feature_property, value):
        self.thing.update_property(feature_property[0], feature_property[1], value)
        print(feature_property[0] + "/" + feature_property[1] + ":" + str(value))

    def save_thing(self):
        self.thing.write_settings()


test = Run()
test.save_thing()
