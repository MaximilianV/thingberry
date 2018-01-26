from thingconnector.thingconnector import ThingConnector
import logging


class Component:
    def __init__(self, **kwargs):
        self.connector = ThingConnector()
        self.logger = logging.getLogger(__name__)
        self.setup_logging()

    @staticmethod
    def setup_logging():
        # Setup logger
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s [%(relativeCreated)6d %(threadName)s] [%(levelname)-5.5s]  %(message)s",
            handlers=[
                logging.FileHandler("{0}/{1}.log".format("logs", "training")),
                logging.StreamHandler()
            ])