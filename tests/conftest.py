import pytest

from src.config import settings
from src.database import Base, engine_null_pool, async_session_maker_null_pool
from src.main import app
from src.models import *
from httpx import AsyncClient
from src.schemas.hotels import HotelAdd
from src.schemas.rooms import RoomAdd
from src.utils.db_manager import DBManager
import json


@pytest.fixture(scope="session", autouse=True)
def check_test_mode():
    assert settings.MODE == "TEST"


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def fillin_data(setup_database):
    with open('mock_hotels.json') as fp:
        hotels = json.load(fp)
    
    with open('mock_rooms.json') as fp:
        rooms = json.load(fp)

    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        for hotel in hotels:
            hotel = HotelAdd(**hotel)
            new_hotel_data = await db.hotels.add(hotel)
        for room in rooms:
            room = RoomAdd(**room)
            new_room_data = await db.rooms.add(room)
        await db.commit()
    

@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_database):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "kot@pes.com",
                "password": "1234"
            }
        )
