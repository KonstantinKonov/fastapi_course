from repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from sqlalchemy import select, insert
from src.api.dependencies import HotelDep


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self, 
            location,
            title,
            limit,
            offset
        ):
        query = select(HotelsOrm)
        if location is not None:
            query = query.filter(HotelsOrm.location.ilike(f'%{location}%'))
        if title is not None:
            query = query.filter_by(title=title). \
                limit(limit). \
                offset(offset)
        query = query. \
            limit(limit). \
            offset(offset)

        res = await self.session.execute(query)
        hotels = res.scalars().all()

        return hotels

    async def add(
              self, 
              hotel_data: HotelDep
        ):
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        res_insert = await self.session.execute(add_hotel_stmt)
        res_select = await self.session.execute(select(HotelsOrm).filter(HotelsOrm.id == res_insert.inserted_primary_key[0]))
        return res_select.scalars().all()