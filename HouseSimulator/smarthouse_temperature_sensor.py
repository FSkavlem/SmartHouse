import logging
import time
import math
from threading import Thread, Lock
from messaging import SensorMeasurement
import common
import json
import requests
class Sensor:

    def __init__(self, did):
        self.did = did
        self.measurement = SensorMeasurement('0.0')
        self.lock = Lock()

    def simulator(self):

        logging.info(f"Sensor {self.did} starting")

        while True:

            temp = round(math.sin(time.time() / 10) * common.TEMP_RANGE, 1)
            with self.lock:
                logging.info(f"Sensor {self.did}: {temp}")
                self.measurement.set_temperature(str(temp))

            time.sleep(common.TEMPERATURE_SENSOR_SIMULATOR_SLEEP_TIME)

    def client(self):

        logging.info(f"Sensor Client {self.did} starting")

        # send temperature to the cloud service with regular intervals
        while True:
            with self.lock:
                measurement = self.measurement

            url = "http://127.0.0.1:8000/smarthouse/sensor/8/current"
            payload = json.dumps({"value": f"{measurement.value}"})
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            time.sleep(common.TEMPERATURE_SENSOR_CLIENT_SLEEP_TIME)

        logging.info(f"Client {self.did} finishing")

        # TODO END

    def run(self):
        # create and start thread simulating physical temperature sensor
        t1 = Thread(target=self.simulator)
        t1.start()

        # create and start thread sending temperature to the cloud service
        t2 = Thread(target=self.client)
        t2.start()


