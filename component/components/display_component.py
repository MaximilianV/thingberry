from component import ActionComponent
from .lib.lcddriver import lcd as LCD


class DisplayComponent(ActionComponent):
    def trigger_action(self, value, **kwargs):
        lcd = LCD()
        lcd.lcd_clear()
        lcd.lcd_display_string(value, 1)

    @staticmethod
    def configure_action():
        print("The Display Action doesn't need to be configured.")
        return {}
