from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.facilities import Facilities, FacilitiesAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get('')
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()

@router.post('')
async def add_facilities(
    db: DBDep,
    data: Facilities
    ):
    await db.facilities.add(data)
    await db.commit()
    return {'status': 'ok'}