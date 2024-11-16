from fastapi import FastAPI, Query, Body

app = FastAPI()

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
    }
]


@app.get('/hotels', summary='Получить список отелей')
def get_items(id: int | None = Query(None, description='id'), title: str | None = Query(None, description='title')):
    hotels_filtered = []
    for hotel in hotels:
        if id and hotel['id'] != id:
            continue
        if title and hotel['title'] != title:
            continue
        hotels_filtered.append(hotel)
    return hotels_filtered


@app.delete('/hotels/{id}', summary='Удаление отеля')
def delete_item(id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel['id'] != id]
    return {'status': 'OK'}


@app.post('/hotels/', summary='Создать новую запись')
def post_hotel(title: str = Body(), city: str = Body()):
    global hotels
    hotels.append(
        {
            'id': hotels[-1]['id'] + 1,
            'title': title,
            'city': city
        }
    )
    return {'status': 'OK'}


@app.put('/hotels/{id}', summary='Обновление записи')
def put_hotel(id: int, title: str = Body(), city: str = Body()):
    global hotels
    for hotel in hotels:
        if hotel['id'] == id:
            hotel['name'] = title
            hotel['city'] = city
    return {'status': 'OK'}


@app.patch('/hotels/{id}', summary='Частичное обновление')
def update_hotel(id: int, title: str | None = Body(None, description='Hotel title'), city: str | None = Body(None, description='Hotel city')):
    global hotels
    for hotel in hotels:
        if hotel['id'] == id:
            if title is not None:
                hotel['title'] = title  
            if city is not None:
                hotel['city'] = city
            break
    return {'status': 'OK'}


import time 
import asyncio


@app.get("/sync/{id}")
def sync_func(id: int):
    print(f'start {id}: {time.time():.2f}')
    time.sleep(3)
    print(f'stop {id}: {time.time():.2f}')


@app.get("/async/{id}")
async def async_func(id: int):
    print(f'start {id}: {time.time():.2f}')
    await asyncio.sleep(3)
    print(f'stop {id}: {time.time():.2f}')