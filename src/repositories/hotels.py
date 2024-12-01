from repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from sqlalchemy import select, insert
from src.api.dependencies import HotelDep
from pydantic import BaseModel, ConfigDict


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


class HodelAdd(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class HotelPatch(BaseModel):
    title: str | None = None
    location: str | None = None