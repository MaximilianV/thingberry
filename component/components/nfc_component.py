from component import ActionComponent, ObserverComponent
from .lib.MFRC522 import MFRC522
import RPi.GPIO as GPIO
import time
import logging


class NfcComponent(ActionComponent, ObserverComponent):
    def trigger_action(self, **kwargs):
        continue_reading = True
        MIFAREReader = MFRC522()

        # This loop keeps checking for chips. If one is near it will get the UID and authenticate
        while continue_reading:
            (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
            if status == MIFAREReader.MI_OK:
                print("Card detected")
            (status, uid) = MIFAREReader.MFRC522_Anticoll()

            if status == MIFAREReader.MI_OK:
                print("Card read UID: " + str(uid[0]) + "," + str(uid[1]) + "," + str(uid[2]) + "," + str(uid[3]))
                # This is the default key for authentication
                key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                # Select the scanned tag
                MIFAREReader.MFRC522_SelectTag(uid)
                # Authenticate
                status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
                print("\n")
                # Check if authenticated
                if status == MIFAREReader.MI_OK:
                    # Variable for the data to write
                    data = []
                    timestamp = str(time.time()).split(".")[0]
                    for x in range(0, 16):
                        if x < len(timestamp):
                            data.append(ord(timestamp[x]))
                        else:
                            data.append(0x00)
                    print("Sector 8 will now be filled with 0xFF:")
                    # Write the data
                    MIFAREReader.MFRC522_Write(8, data)
                    # Stop
                    MIFAREReader.MFRC522_StopCrypto1()
                    # Make sure to stop reading for cards
                    self.connector.reset_action(self.thing_id, self.action_name)
                    continue_reading = False
                else:
                    print("Authentication error")

    def observe(self, **kwargs):
        continue_reading = True
        # Create an object of the class MFRC522
        MIFAREReader = MFRC522()
        last_read_value = ""
        # This loop keeps checking for chips. If one is near it will get the UID and authenticate
        while continue_reading:
            (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
            # If a card is found
            if status == MIFAREReader.MI_OK:
                print("Card detected")
            # Get the UID of the card
            (status, uid) = MIFAREReader.MFRC522_Anticoll()
            # If we have the UID, continue
            if status == MIFAREReader.MI_OK:
                # Print UID
                print("Card read UID: " + str(uid[0]) + "," + str(uid[1]) + "," + str(uid[2]) + "," + str(uid[3]))
                # This is the default key for authentication
                key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                # Select the scanned tag
                MIFAREReader.MFRC522_SelectTag(uid)
                # Authenticate
                status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)
                # Check if authenticated
                if status == MIFAREReader.MI_OK:
                    data = MIFAREReader.MFRC522_Read(8)
                    MIFAREReader.MFRC522_StopCrypto1()
                    card_value = ""
                    for x in data:
                        if x != 0:
                            card_value += chr(x)
                    if card_value == "":
                        card_value = "0"
                    logging.info("Read " + card_value)
                    if card_value != last_read_value:
                        last_read_value = card_value
                        logging.info("Updated thing")
                        nfc_feature_content = dict()
                        nfc_feature_content["properties"] = dict()
                        nfc_feature_content["properties"]["lastTriggered"] = self.get_timestamp()
                        nfc_feature_content["properties"]["lastReadId"] = card_value
                        self.connector.update_feature(self.thing_id, self.feature_name, nfc_feature_content)
                    else:
                        logging.info("No updated needed")
                else:
                    print("Authentication error")
            time.sleep(1)

    @staticmethod
    def configure_action():
        print("The NFC Action doesn't need to be configured.")
        return {}

    @staticmethod
    def configure_observer():
        print("The NFC Observer doesn't need to be configured.")
        return {}
