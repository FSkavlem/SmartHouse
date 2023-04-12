from pydantic import BaseModel

from House.Demohouse.room import Room


class Floor (BaseModel):

    fid: int
    level: int
    rooms: list[Room]
