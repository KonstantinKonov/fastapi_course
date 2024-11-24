from fastapi import APIRouter, Body, Query

from src.api.dependencies import PaginationDep, HotelDep, HotelPatchDep


router = APIRouter(prefix='/hotels', tags=['Hotels'])


hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@router.get('/')
async def get_hotels(
    pagination: PaginationDep,
    id: int = Query(None, description='Hotel Id'),
    title: str | None = Query(None, description='Hotel Title'),
):
    hotels_filtered = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_filtered.append(hotel)
    
    if pagination.page and pagination.per_page:
        start = pagination.per_page * (pagination.page - 1)
        end = pagination.per_page * pagination.page
        return hotels_filtered[start : end]
    return hotels_filtered


@router.post('/')
async def post_hotel(
    hote_id: int,
    hotel_data: HotelDep
):
    global hotels
    hotels.append(
        {
            'id': hotels[-1]['id'],
            'title': hotel_data.title,
            'name': hotel_data.name
        }
    )
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