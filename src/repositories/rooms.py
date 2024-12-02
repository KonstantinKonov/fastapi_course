from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from sqlalchemy import select, insert, update
from src.api.dependencies import RoomDep
from pydantic import BaseModel
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

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