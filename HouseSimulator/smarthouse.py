import logging

from HouseSimulator.smarthouse_temperature_sensor import Sensor
from HouseSimulator.smarthouse_lightbulb import Actuator
from multiprocessing import current_process

import common


def run():
    print(current_process().name)
    log_format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=log_format, level=logging.INFO, datefmt="%H:%M:%S")

    sensor = Sensor(common.TEMPERATURE_SENSOR_DID)
    sensor.run()

    actuator = Actuator(common.LIGHTBULB_DID)
    actuator.run()

