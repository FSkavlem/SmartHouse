from House.houseAPI import ApiServer
from multiprocessing import Process, current_process
from HouseSimulator import smarthouse
from HouseDashboard import dashboard


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


