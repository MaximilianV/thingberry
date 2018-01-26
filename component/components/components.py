from enum import Enum
from .camera_component import CameraComponent
from .display_component import DisplayComponent
from .vibration_component import VibrationComponent
from .nfc_component import NfcComponent
from .button_component import ButtonComponent


class Components(Enum):
    Camera = CameraComponent
    Button = ButtonComponent
    NFC = NfcComponent
    Vibration = VibrationComponent
    Display = DisplayComponent
