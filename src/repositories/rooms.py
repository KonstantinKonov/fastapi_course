from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from sqlalchemy import select, insert, update
from src.api.dependencies import RoomDep
from pydantic import BaseModel



class RoomsRepository(BaseRepository):
    model = RoomsOrm

    async def get_all(
            self, 
            hotel_id,
            title,
            description,
            price,
            quantity
        ):
        query = select(RoomsOrm)
        if title is not None:
            query = query.filter(RoomsOrm.title.ilike(f'%{title}%'))
        if description is not None:
            query = query.filter(RoomsOrm.descriptiotn.ilike(f'%{description}%'))
        
        res = await self.session.execute(query)
        rooms = res.scalars().all()

        return rooms


    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by):
        update_hotel_stmt = update(self.model) \
        .where(self.model.id==filter_by['id']) \
        .where(self.model.hotel_id==filter_by['hotel_id']) \
        .values(**data.model_dump(exclude_unset=exclude_unset))
        res = await self.session.execute(update_hotel_stmt)
        return None