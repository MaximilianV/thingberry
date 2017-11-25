from propertyobserver.file_intervalobserver import FileIntervalObserver
from threading import Timer


class Run():
    def start(self):
        fileobs = FileIntervalObserver("test.json", feature_property="test", runner=self)
        fileobs.start()
        t = Timer(10.0, fileobs.stop)
        t.start()
        fileobs.join()

    def notify(self, feature_property, value):
        print(feature_property + ":" + str(value))
