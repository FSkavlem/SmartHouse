from pydantic import BaseModel

from House.Demohouse.device import Device


class Room(BaseModel):

    rid: int
    area: float
    name: str
    devices: list[Device]

