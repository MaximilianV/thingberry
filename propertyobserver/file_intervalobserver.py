from .intervalobserver import IntervalObserver
import json


class FileIntervalObserver(IntervalObserver):
    def __init__(self, file_path, *args, **kwargs):
        self.file_path = file_path
        super(FileIntervalObserver, self).__init__(*args, **kwargs)

    def observe(self):
        with open(self.file_path, 'r') as fp:
            self.notify(json.load(fp))