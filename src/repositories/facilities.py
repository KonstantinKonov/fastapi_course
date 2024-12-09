from sqlalchemy import select, func

from src.repositories.base import BaseRepository
from src.schemas.facilities import Facilities
from src.models.facilities import FacilitiesOrm


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facilities