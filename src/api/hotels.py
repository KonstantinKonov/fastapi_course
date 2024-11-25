from fastapi import APIRouter, Body, Query

from src.api.dependencies import PaginationDep, HotelDep, HotelPatchDep
from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from sqlalchemy import insert, select
from repositories.hotels import HotelsRepository


router = APIRouter(prefix='/hotels', tags=['Hotels'])


@router.get('/')
async def get_hotels(
    pagination: PaginationDep,
    location: str | None = Query(None, description='Hotel Location'),
    title: str | None = Query(None, description='Hotel Title'),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location, 
            title, 
            limit=per_page,
            offset=per_page * (pagination.page - 1)
            )
    

@router.post('/')
async def post_hotel(
    hote_id: int,
    hotel_data: HotelDep
):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {'status': 'OK', 'data': hotel}


@router.put('/{id}')
async def put_hotel(
    id: int,
    hotel_data: HotelDep
):
    global hotels
    hotel = next(filter(lambda hotel : hotel['id'] == id, hotels))
    hotel['title'] = hotel_data.title
    hotel['name'] = hotel_data.name
    return {'status': 'OK'}


@router.patch('/{id}')
async def update_hotel(
    id: int,
    hotel_data: HotelPatchDep
):
    global hotels
    hotel = next(filter(lambda hotel : hotel['id'] == id, hotels))
    if hotel_data.title:
        hotel['title'] = hotel_data.title
    if hotel_data.name:
        hotel['name'] = hotel_data.name
    return {'status': 'OK'}


@router.delete('/{id}')
async def delete(
    id: int
):
    global hotels
    hotels = list(filter(lambda hotel : hotel['id'] != id, hotels))
    return {'status': 'OK'}