from fastapi import FastAPI, Query, APIRouter
from schemas.hotels import Hotel, HotelPatch

router = APIRouter(prefix='/hotels', tags=["Отели"])

hotels = [
    {
        'id': 1,
        'title': 'Legendary Leisure',
        'city': 'Sochi'
    },
    {
        'id': 2,
        'title': 'Dubai dubbing',
        'city': 'Dubai'
    },
    {
        'id': 3,
        'title': 'kazan plaza',
        'city': 'kazan'
    },
    {
        'id': 4,
        'title': 'moscow',
        'city': 'moscow cow'
    },
    {
        'id': 5,
        'title': 's-p',
        'city': 'sankt-peterburg'
    },
    {
        'id': 6,
        'title': 'minsk',
        'city': 'minsk'
    },
    {
        'id': 7,
        'title': 'kiev',
        'city': 'Kiev'
    }
]


@router.get('/', summary='Получить список отелей')
def get_items(
    id: int | None = Query(None, description='id'), 
    title: str | None = Query(None, description='title'), 
    page: int | None = Query(1, description='startpage'), 
    per_page: int | None = Query(3, description='per page')
    ):

    hotels_filtered = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_filtered.append(hotel)
        
    hotels_filtered = hotels_filtered[(page-1) * per_page : page*per_page]
    return hotels_filtered


@router.delete('//{id}', summary='Удаление отеля')
def delete_item(id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != id]
    return {'status': 'OK'}


@router.post('/', summary='Создать новую запись')
def post_hotel(hotel_data: Hotel):
    global hotels
    hotels.append(
        {
            'id': hotels[-1]['id'] + 1,
            'title': hotel_data.title,
            'city': hotel_data.city 
        }
    )
    return {'status': 'OK'}


@router.put('/{id}', summary='Обновление записи')
def put_hotel(id: int, hotel_data: Hotel):
    global hotels
    for hotel in hotels:
        if hotel['id'] == id:
            hotel['name'] = hotel_data.title 
            hotel['city'] = hotel_data.city
    return {'status': 'OK'}


@router.patch('/{id}', summary='Частичное обновление')
def update_hotel(id: int, hotel_data: HotelPatch):
    global hotels
    for hotel in hotels:
        if hotel['id'] == id:
            if hotel_data.title is not None:
                hotel['title'] = hotel_data.title  
            if hotel_data.city is not None:
                hotel['city'] = hotel_data.city
            break
    return {'status': 'OK'}