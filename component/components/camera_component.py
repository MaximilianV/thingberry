from component import ActionComponent
import logging
from picamera import PiCamera
from time import sleep
import random
import string
import socket


class CameraComponent(ActionComponent):
    def trigger_action(self, **kwargs):
        delay = int(self.action_config["delay"])
        if delay == 0:
            delay = 1
        destination = self.action_config["destination"]
        logging.info("Taking a photo in " + str(delay) + " seconds.")
        filename = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        filename += '.jpg'
        camera = PiCamera()
        sleep(delay)
        image_destination = destination + filename
        camera.capture(image_destination)
        logging.info("Photo taken and stored in " + str(image_destination) + ".")
        camera.close()
        self.connector.reset_action(self.thing_id, self.action_name)
        ip_address = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
                                    if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)),
                                                                          s.getsockname()[0], s.close()) for s in
                                                                         [socket.socket(socket.AF_INET,
                                                                                        socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
        camera_feature_content = dict()
        camera_feature_content["properties"] = dict()
        camera_feature_content["properties"]["lastTriggered"] = self.get_timestamp()
        camera_feature_content["properties"]["lastPictureUrl"] = "http://" + ip_address + "/images/" + filename
        logging.info(self.connector.update_feature(self.thing_id, "camera", camera_feature_content))

    @staticmethod
    def configure_action():
        print("Configuring Camera Action:")
        delay = int(input("Delay until photo is taken (def. 2): "))
        destination = input("Destination to save image: ")
        ip_address = input("What's the current IP address?")
        return {
            "delay": delay,
            "destination": destination
        }
