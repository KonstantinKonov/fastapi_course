from fastapi import APIRouter, Body, Query

from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch
from src.database import async_session_maker

from src.repositories.rooms import RoomsRepository
from src.api.dependencies import DBDep


router = APIRouter(prefix='/rooms', tags=['Rooms'])


# get all
@router.get('/{hotel_id}/rooms')
async def get_rooms(
    hotel_id: int,
    db: DBdep
):
    return await db.rooms.get_fitered(hote_id=hotel_id)


# get room
@router.get('/{hotel_id}/rooms/{room_id}')
async def get_room(
    hotel_id: int,
    room_id: int,
    db: DBDep
    ):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


# create room
@router.post('/{hotel_id}/rooms')
async def post_room(
    hotel_id: int,
    db: DBDep,
    room_data: RoomAddRequest = Body()
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)
    await db.commit()

    return {'status': 'OK', 'data': room}


# edit room
@router.put('/{hotel_id}/rooms/{id}')
async def edit_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
    db: DBDep
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    await db.commit()

    return {'status': 'OK'}


# patch room
@router.patch('/{hotel_id}/rooms/{id}')
async def patch_room(
    hotel_id:int,
    room_id: int,
    room_data: RoomAddRequest,
    db: DBDep
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, exclude_unset=True, id=room_id, hotel_id=hotel_id)
    await db.commit()

    return {'status': 'OK'}


# delete room
@router.delete('/{hotel_id}/rooms/{id}')
async def delete(
    hotel_id: int,
    room_id: int,
    db: DBDep
):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commmit()

    return {'status': 'OK'}