from enum import Enum
from propertyobserver.intervalobserver import IntervalObserver


class PropertyObserverFactory:

    @staticmethod
    def create_observer(observer_style, observer, feature_property, config):
        if observer_style == ObserverStyle.INTERVAL:
            observer = IntervalObserver(interval=config["interval"], observer=observer, feature_property=feature_property)
        return observer


class ObserverStyle(Enum):
    INTERVAL = IntervalObserver
