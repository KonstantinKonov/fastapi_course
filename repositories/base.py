from sqlalchemy import select
from src.models.hotels import HotelsOrm


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self):
        query = select(HotelsOrm)
        result = await self.session.execute(query)

        return result.scalars().all()


    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)

        return result.scalars().one_or_none()


