from fastapi import APIRouter, Body, Query

from src.api.dependencies import PaginationDep, HotelDep, HotelPatchDep
from src.database import async_session_maker
#from src.models.hotels import HotelsOrm
#from src.models.rooms import RoomsOrm
from sqlalchemy import insert, select
from src.repositories.hotels import HotelsRepository, HotelAdd, HotelPatch
from src.api.dependencies import DBDep
from src.utils.db_manager import DBManager


router = APIRouter(prefix='/hotels', tags=['Hotels'])


@router.get('/')
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    location: str | None = Query(None, description='Hotel Location'),
    title: str | None = Query(None, description='Hotel Title'),
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all(
        location, 
        title, 
        limit=per_page,
        offset=per_page * (pagination.page - 1)
        )
    

@router.get('/{hotel_id}')
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post('/')
async def post_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body()
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {'status': 'OK', 'data': hotel}


@router.put('/{hotel_id}')
async def edit_hotel(
    hotel_id: int,
    hotel_data: HotelAdd,
    db: DBDep
):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()

    return {'status': 'OK'}


@router.patch('/{hotel_id}')
async def patch_hotel(
    hotel_id: int,
    hotel_data: HotelPatch,
    db: DBDep
):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()

    return {'status': 'OK'}


@router.delete('/{hotel_id}')
async def delete(
    hotel_id: int,
    db: DBDep
):
    await db.hotels.delete(id=hotel_id)
    await db.commit()

    return {'status': 'OK'}