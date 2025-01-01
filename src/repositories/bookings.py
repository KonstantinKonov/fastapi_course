from datetime import date

from sqlalchemy import select
from fastapi import HTTPException

from src.models.bookings import BookingsOrm
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper
from src.repositories.utils import rooms_ids_for_booking

class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = (
            select(BookingsOrm)
            .filter(BookingsOrm.date_from == date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(self, date_from, date_to, hotel_id):
        ids = rooms_ids_for_booking(date_from, date_to, hotel_id)
        if not ids:
            raise HTTPException(status_code=404, detail="No free rooms")

        booking = BookingsOrm(
            room_id=ids[0],
            user_id=self.model.user_id,
            date_from=self.model.date_from,
            date_to=self.model.date_to,
            description=self.model.description,
            price=self.model.price
        )
        self.session.add(booking)
        await self.session.commit()

        return booking
