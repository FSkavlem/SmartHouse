import uvicorn
from fastapi import FastAPI, HTTPException
from House.Demohouse.housebuilder import build_demo_house
from House.Demohouse.sensors import *
from House.Demohouse.actuators import *

from multiprocessing import current_process

# in fastAPI we can send json or python dictonary(dict will automaticly be converted to json)
class ApiServer:

    def run(self):
        uvicorn.run(self.app, host="127.0.0.1", port=8000)

    def __init__(self):
        self.app = FastAPI()
        self.smart_house = build_demo_house()
        print(current_process().name)
        # http://localhost:8000/

        @self.app.get('/ok')
        def ok():
            return {"OK"}

        @self.app.get("/")
        async def root():
            return {"message": "Welcome to SmartHouse Cloud REST API - Powered by FastAPI"}


        @self.app.get("/smarthouse")
        async def smarthouse():
            """information on the smart house"""
            return self.smart_house#self.smart_house


        @self.app.get("/smarthouse/floor")
        async def smarthouse():
            """ information on all floors"""
            return self.smart_house.floors


        @self.app.get("/smarthouse/floor/{fid}")
        async def smarthouse(fid: int):
            """information about a floor given by fid"""
            try:
                return self.smart_house.floors[fid]
            except IndexError:
                raise HTTPException(status_code=404, detail="Index out of range")


        @self.app.get("/smarthouse/floor/{fid}/room")
        async def smarthouse(fid: int):
            """information about all rooms on a given floor fid"""
            try:
                return self.smart_house.floors[fid].rooms
            except IndexError:
                raise HTTPException(status_code=404, detail="Index out of range")


        @self.app.get("/smarthouse/floor/{fid}/room/{rid}")
        async def smarthouse(fid: int, rid: int):
            """information about a specific room rid on a given floor fid"""
            try:
                return self.smart_house.floors[fid].rooms[rid]
            except IndexError:
                raise HTTPException(status_code=404, detail="Index out of range")


        @self.app.get("/smarthouse/device")
        async def device():
            """information on all devices"""
            return self.smart_house.get_all_devices()

        @self.app.get("/smarthouse/device/{did}")
        async def device(did: int):
            """information for a given device did"""
            try:
                return self.smart_house.get_all_devices()[did]
            except KeyError:
                raise HTTPException(status_code=404, detail="No such device id")


        @self.app.get("/smarthouse/sensor/{did}/current")
        async def sensor(did: int):
            """get current sensor measurement for sensor did"""
            try:
                return {"value": self.smart_house.get_all_devices()[did].get_current_value()}
            except KeyError:
                raise HTTPException(status_code=404, detail="No such device id")
            except AttributeError:
                raise HTTPException(status_code=400, detail="Device requested is not a sensor")


        @self.app.post("/smarthouse/sensor/{did}/current", status_code=201)
        async def sensor(did: int, measurement: SensorMeasurement):
            """add measurement for sensor did
            POST BODY
            {
            "value": "9"
            }
            """
            try:
                self.smart_house.get_all_devices()[did].set_current_value(float(measurement.value))
                return {"success": "Measurement value {0} added to device {1}".format(measurement.value, did)}
            except KeyError:
                raise HTTPException(status_code=404, detail="No such device id")
            except AttributeError:
                raise HTTPException(status_code=400, detail="Device requested is not a sensor")
            except ValueError:
                raise HTTPException(status_code=400, detail="Value entered not a valid value")


        @self.app.get("/smarthouse/sensor/{did}/values")
         # values?limit=10
        async def sensor(did: int, limit: int = -1):
            """get all available measurements for sensor did"""
            try:
                x = self.smart_house.get_all_devices()[did].get_current_values()
                if limit != -1:
                    x = x[:limit]
                y = zip(range(0, len(x)), x)
                return dict(y)
            except KeyError:
                raise HTTPException(status_code=404, detail="No such device id")
            except AttributeError:
                raise HTTPException(status_code=400, detail="Device requested is not a sensor")

        @self.app.delete("/smarthouse/sensor/{did}/oldest", status_code=200)
        async def sensor(did: int):
            """delete oldest measurements for sensor did"""
            try:
                self.smart_house.get_all_devices()[did].delete_oldest_value()
                return {"success": "Oldest measurement deleted!"}
            except KeyError:
                raise HTTPException(status_code=404, detail="No such device id")
            except AttributeError:
                raise HTTPException(status_code=400, detail="Device requested is not a sensor")
            except IndexError:
                raise HTTPException(status_code=400, detail="Sensor contains no readings")


        @self.app.get("/smarthouse/actuator/{did}/current")
        async def actuator(did: int):
            """ get current state for actuator did"""
            try:
                x = self.smart_house.get_all_devices()[did]
                return {"actuator {0} state".format(x.nickname): x.get_current_state()}
            except KeyError:
                raise HTTPException(status_code=404, detail="No such device id")
            except AttributeError:
                raise HTTPException(status_code=400, detail="Device requested is not a actuator")


        @self.app.put("/smarthouse/device/{did}")
        async def actuator(did: int, activation: ActuatorState):
            """ update current state for actuator did"""
            try:
                x = self.smart_house.get_all_devices()[did]
                x.set_current_state(activation.state)
                return {"success": "state of device {0} set to {1}".format(x.nickname, activation.state)}
            except KeyError:
                raise HTTPException(status_code=404, detail="No such device id")
            except AttributeError:
                raise HTTPException(status_code=400, detail="Device requested is not a actuator")
            except ValueError:
                raise HTTPException(status_code=400, detail="Device is not controlled by on off")



