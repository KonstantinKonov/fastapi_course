from fastapi import APIRouter, Body, Query

from src.schemas.rooms import RoomDep, RoomPatchDep
from src.database import async_session_maker

from src.repositories.rooms import RoomsRepository


router = APIRouter(prefix='/rooms', tags=['Rooms'])


@router.get('/{hotel_id}')
async def get_rooms(
    hotel_id: int,
    title: str | None = Query(None),
    description: str | None = Query(None),
    price: int | None = Query(None),
    quantity: int | None = Query(None)
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            hotel_id,
            title,
            description,
            price,
            quantity
        )


@router.get('/{hotel_id}/{room_id}')
async def get_room(
    hotel_id: int,
    id: int
    ):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(hotel_id=hotel_id, id=id)


@router.post('/{hotel_id}')
async def post_room(
    room_data: RoomDep
):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()


@router.put('/{hotel_id}/{id}')
async def edit_room(
    id: int,
    room_data: RoomDep
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, exclude_unset=False, id=id)
        await session.commit()
    return {'status': 'OK'}


@router.patch('/{hotel_id}/{id}')
async def patch_room(
    hotel_id:int,
    id: int,
    room_data: RoomPatchDep
):
    async with async_session_maker() as session:
        #res = await RoomsRepository(session).get_one_or_none(hotel_id=hotel_id, id=id)
        #res = await res.edit(room_data)
        await RoomsRepository(session).edit(room_data, exclude_unset=True, id=id, hotel_id=hotel_id)
        await session.commit()
    return {'status': 'OK'}


@router.delete('/{hotel_id}/{id}')
async def delete(
    id: int
):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=id)
        await session.commit()
    return {'status': 'OK'}