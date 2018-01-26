from component import ObserverComponent
import logging
import RPi.GPIO as GPIO


class ButtonComponent(ObserverComponent):
    def start_observe(self, **kwargs):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(int(self.property_config["pin"]), GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(int(self.property_config["pin"]), GPIO.RISING)
        super().start_observe(**kwargs)

    def observe(self, initial_count=0, **kwargs):
        count = initial_count
        while True:
            channel = GPIO.wait_for_edge(int(self.property_config["pin"]), GPIO.RISING)
            if channel:
                logging.debug("Detected button press for: " + self.property_name)
                count += 1
                self.update_property(count)

    @staticmethod
    def configure_observer():
        print("Configuring Button Property:")
        pin = int(input("Which pin is the button connected to?"))
        return {
            "pin": pin,
        }
