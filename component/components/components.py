from enum import Enum
from component.components import *


class Component(Enum):
    Camera = CameraComponent
    Button = ButtonComponent
    NFC = NfcComponent
    Vibration = VibrationComponent
    Display = DisplayComponent
