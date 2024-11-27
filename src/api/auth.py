from fastapi import APIRouter

from passlib.context import CryptContext

from src.repositories.users import UsersRepository
from src.database import async_session_maker
from src.schemas.users import UserRequestAdd, UserAdd


router = APIRouter(prefix='/auth', tags=['Autherization and authentication'])

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

@router.post('/registre')
async def register_user(
    data: UserRequestAdd,
):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        try:
            await UsersRepository(session).add(new_user_data)
            await session.commit()
        except Exception:
            return {'status': 'email already exists'}

    return {'status': 'OK'}