from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from src.config import settings
from sqlalchemy import text
import asyncio
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(settings.DB_URL)

# сессии (трансакции?)
async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

session = async_session_maker()

#await session.execute();

# асинхронное подключение через connection
'''
async def func():
    async with engine.begin() as conn:
        res = await conn.execute(text('SELECT version();'))
        print(res.fetchone())

asyncio.run(func())
'''

class BaseOrm(DeclarativeBase):
    pass