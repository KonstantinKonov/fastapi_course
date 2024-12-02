from fastapi import APIRouter, Body, Query, Request, HTTPException
import datetime as dt
from src.api.dependencies import DBDep
from src.schemas.bookings import Bookings
from src.services.auth import AuthService


router = APIRouter(prefix='/bookings', tags=['Bookings'])

@router.post('')
def add_booking(
    request: Request,
    date_from: dt.date,
    date_to: dt.date,
    room_id: int
):
    room = DBDep.rooms.get_one_or_none(room_id=room_id)
    access_token = request.cookies.get('access_token')
    data = AuthService().decode_token(access_token)
    user_id = data.get('user_id')
    if room is not None and user_id is not None:
        price = room.price * (date_from - date_to).days()
        booking_data = Bookings(room_id=room_id, user_id=user_id)
        DBDep.bookings.add(room_id=room_id, user_id=user_id, date_from=date_from, date_to=date_to, price=price)
        return {'status': 'OK'}
    else:
        raise HTTPException(status_code=401, detail='incorrect password')
