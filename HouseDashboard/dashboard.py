import tkinter as tk

import logging
from multiprocessing import current_process
from HouseDashboard.dashboard_lightbulb import init_lightbulb
from HouseDashboard.dashboard_temperaturesensor import init_temperature_sensor

import common


def run():
    print(current_process().name)
    log_format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=log_format, level=logging.INFO, datefmt="%H:%M:%S")

    root = tk.Tk()
    root.geometry('300x300')
    root.title('ING301 SmartHouse Dashboard')

    init_lightbulb(root, common.LIGHTBULB_DID)
    init_temperature_sensor(root, common.TEMPERATURE_SENSOR_DID)

    root.mainloop()
