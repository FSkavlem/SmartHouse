from pydantic import BaseModel

from House.Demohouse.floor import Floor


class SmartHouse (BaseModel):

    name: str
    floors: list[Floor]
    def get_all_devices(self):
        """Gir tilbake en liste med alle enheter som er registrert i huset."""
        somedict = {}
        for floor in self.floors:
            for room in floor.rooms:
                for device in room.devices:
                    somedict[device.did] = device
        return somedict

