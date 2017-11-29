from enum import Enum
from propertyobserver.intervalobserver import IntervalObserver


class PropertyObserverFactory:

    @staticmethod
    def create_observer(observer_type, observer):
        pass


class ObserverStyle(Enum):
    INTERVAL = IntervalObserver
