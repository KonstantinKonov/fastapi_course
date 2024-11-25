from fastapi import APIRouter, Body, Query

from src.api.dependencies import PaginationDep, HotelDep, HotelPatchDep
from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from sqlalchemy import insert, select

router = APIRouter(prefix='/hotels', tags=['Hotels'])


@router.get('/')
async def get_hotels(
    pagination: PaginationDep,
    location: str | None = Query(None, description='Hotel Location'),
    title: str | None = Query(None, description='Hotel Title'),
):
    per_page = pagination.per_page or 5
    limit = per_page
    offset = per_page * (per_page - 1)
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if location is not None:
            query = query.filter(HotelsOrm.location.ilike(f'%{location}%'))
        if title is not None:
            query = query.filter_by(title=title). \
            limit(limit). \
            offset(offset)
        res = await session.execute(query)
        hotels = res.scalars().all()
        return hotels

    #if pagination.page and pagination.per_page:
        #start = pagination.per_page * (pagination.page - 1)
        #end = pagination.per_page * pagination.page
        #return hotels_filtered[start : end]
    #return hotels_filtered


@router.post('/')
async def post_hotel(
    hote_id: int,
    hotel_data: HotelDep
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {'status': 'OK'}


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