import logging
from threading import Thread, Lock
import time
import requests

from messaging import ActuatorState
import common


class Actuator:

    def __init__(self, did):
        self.did = did
        self.state = ActuatorState('False')
        self.lock = Lock()

    def simulator(self):

        logging.info(f"Actuator {self.did} starting")

        while True:
            with self.lock:
                logging.info(f"Actuator {self.did}: {self.state.state}")
            time.sleep(common.LIGHTBULB_SIMULATOR_SLEEP_TIME)

    def client(self):

        logging.info(f"Actuator Client {self.did} starting")

        # send request to cloud service with regular intervals and
        # set state of actuator according to the received response
        while True:
            response = requests.request("GET", 'http://127.0.0.1:8000/smarthouse/actuator/1/current')
            value = response.json().pop(next(iter(response.json())))
            with self.lock:
                self.state = ActuatorState(value)
            time.sleep(common.LIGHTBULB_CLIENT_SLEEP_TIME)
        logging.info(f"Client {self.did} finishing")

    def run(self):
        # start thread simulating physical light bulb
        t1 = Thread(target=self.simulator)
        t1.start()

        # start thread receiving state from the cloud
        t2 = Thread(target=self.client)
        t2.start()


