from component import ObserverComponent
import logging
import RPi.GPIO as GPIO
import time


class ButtonComponent(ObserverComponent):
    def start_observe(self, **kwargs):
        channel = int(self.property_config["pin"])
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(int(self.property_config["pin"]), GPIO.RISING, bouncetime=300)
        logging.info("Add button press detection on channel " + str(channel))
        super().start_observe(channel=channel)

    def observe(self, channel):
        while True:
            if GPIO.event_detected(channel):
                logging.info("Detected button press for: " + self.property_name)
                self.update_property(self.get_timestamp())
            time.sleep(0.25)

    @staticmethod
    def configure_observer():
        print("Configuring Button Property:")
        pin = int(input("Which pin is the button connected to? "))
        return {
            "pin": pin,
        }
