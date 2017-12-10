from enum import Enum
from propertyobserver.intervalobserver import IntervalObserver
from propertyobserver.permanentobserver import PermanentObserver


class PropertyObserverFactory:

    @staticmethod
    def create_observer(observer_style, observer, config, feature_property):
        if observer_style == ObserverStyle.INTERVAL:
            observer = IntervalObserver(interval=5000, observer=observer, feature_property=feature_property, config=config)
        return observer


class ObserverStyle(Enum):
    INTERVAL = IntervalObserver
    PERMANENT = PermanentObserver
