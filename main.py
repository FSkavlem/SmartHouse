from House.houseAPI import ApiServer
from multiprocessing import Lock, Process, current_process
from HouseSimulator import smarthouse
from HouseDashboard import dashboard

import time
import requests

def runHouseAPI():
    server = ApiServer()
    server.run()

if __name__ == '__main__':
    print(current_process().name)
    p1 = Process(target=runHouseAPI, name='HouseProcess')
    p2 = Process(target=smarthouse.run, name='SimulatorProcess')
    p3 = Process(target=dashboard.run, name='dashboardProces')
    p1.start()
    p2.start()
    p3.start()
    #string = '.'
    #while True:
    #    response = requests.request("GET", 'http://127.0.0.1:8000/ok')
    #    if response.content == b"OK":
    #        break
    #    print("waiting for houseAPI server to deploy") + string
    #    string += '.'
    #    time.sleep(0.5)


