from datetime import date

from src.schemas.bookings import BookingAdd


async def test_add_booking(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2024, month=8, day=10),
        date_to=date(year=2024, month=8, day=20),
        price=100,
    )
    await db.bookings.add(booking_data)

    # получить эту бронь
    booking_receive = await db.bookings.get_one_or_none(user_id=user_id, room_id=room_id)
    assert booking_receive
    # delete key id
    booking_receive = booking_receive.model_dump()
    booking_receive.pop('id')
    assert booking_receive == booking_data.model_dump()

    # обновить бронь
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2025, month=1, day=1),
        date_to=date(year=2025, month=2, day=2),
        price=200
    )
    await db.bookings.edit(data=booking_data, exclude_unset=True, user_id=user_id, room_id=room_id)
    booking_receive = await db.bookings.get_one_or_none(user_id=user_id, room_id=room_id)
    assert booking_receive
    # delete key id
    booking_receive = booking_receive.model_dump()
    booking_receive.pop('id')
    assert booking_receive == booking_data.model_dump()

    # удалить бронь
    id = (await db.bookings.get_one_or_none(user_id=user_id, room_id=room_id)).id
    await db.bookings.delete(id=id)
    booking_receive = await db.bookings.get_one_or_none(id=id)
    assert booking_receive is None

    await db.commit()
