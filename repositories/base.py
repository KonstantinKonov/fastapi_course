from sqlalchemy import select, insert, delete, update
from src.models.hotels import HotelsOrm
from src.api.dependencies import BaseModel


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


    async def add(self, data: BaseModel):
        add_hotel_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        res = await self.session.execute(add_hotel_stmt)
        return res.scalars().one()


    async def edit(self, data: BaseModel, **filter_by):
        update_hotel_stmt = update(self.model).where(self.model.id==filter_by['id']).values(**data.model_dump())
        res = await self.session.execute(update_hotel_stmt)
        return None


    async def delete(self, **filter_by):
        delete_hotel_stmt = delete(self.model).where(self.model.id==filter_by['id'])
        res = await self.session.execute(delete_hotel_stmt)
        return None