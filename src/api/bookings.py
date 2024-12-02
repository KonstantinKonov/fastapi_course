from fastapi import APIRouter, Body, Query, Request, HTTPException
import datetime as dt
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import Booking, BookingAdd, BookingAddRequest


router = APIRouter(prefix='/bookings', tags=['Bookings'])


@router.post('')
async def add_booking(
    user_id: UserIdDep,
    booking_data: BookingAddRequest,
    db: DBDep
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price = room.price
    _booking_data = BookingAdd(
        user_id=user_id,
        price=...,
        **booking_data.model_dump()
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()

    return {'status': 'OK', 'data': booking}


@router.get('')
async def get_bookings(
    db: DBDep
):
    return await db.bookings.get_all()


@router.get('/me')
async def get_my_bookings(
    user_id: UserIdDep,
    db: DBDep
):
    return await db.bookings.get_one_or_none(user_id=user_id)
