from typing import Annotated
from fastapi import Depends
from pydantic import BaseModel, Field


class Room(BaseModel):
    hotel_id: int
    title: str
    description: str
    price: int
    quantity: int


class RoomPatch(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)


RoomDep = Annotated[Room, Depends()]
RoomPatchDep = Annotated[RoomPatch, Depends()]