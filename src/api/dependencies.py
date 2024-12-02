from typing import Annotated
from fastapi import Depends, Query, Body, HTTPException, Request
from pydantic import BaseModel

from src.database import async_session_maker
from src.services.auth import AuthService
from src.utils.db_manager import DBManager

class PaginationParams(BaseModel):
    page: Annotated[int, Query(1, gt=0)]
    per_page: Annotated[int | None, Query(None, ge=1, lt=30)]


class Hotel(BaseModel):
    title: Annotated[str, Body()]
    location: Annotated[str, Body()]


class HotelPatch(BaseModel):
    title: Annotated[str | None, Body()]
    location: Annotated[str | None, Body()]


class Room(BaseModel):
    title: Annotated[str, Body()]
    description: Annotated[str, Body()]
    price: Annotated[int, Body()]
    quantity: Annotated[int, Body()]


class RoomPatch(BaseModel):
    title: Annotated[str | None, Body()]
    description: Annotated[str | None, Body()]
    price: Annotated[int | None, Body()]
    quantity: Annotated[int | None, Body()]


RoomDep = Annotated[Room, Depends()]
RoomPatchDep = Annotated[RoomPatch, Depends()]


PaginationDep = Annotated[PaginationParams, Depends()]
#HotelDep = Annotated[Hotel, Depends()]
#HotelPatchDep = Annotated[HotelPatch, Depends()]


def get_token(request: Request) -> str:
    token = request.cookies.get('access_token')
    if not token:
        raise HTTPException(status_code=401, detail='token required')
    return token


def get_current_user_id(token: str = Depends(get_token)) -> int:
    data = AuthService().encode_token(token)
    return data['user_id']


UserIdDep = Annotated[int, Depends(get_current_user_id)]


def get_db_manager():
    return DBManager(session_factory=async_session_maker)


async def get_db():
    async with get_db_manager() as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]