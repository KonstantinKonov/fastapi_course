from fastapi import APIRouter, HTTPException, Response, Request
from starlette.requests import Request

from src.repositories.users import UsersRepository
from src.database import async_session_maker
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix='/auth', tags=['Autherization and authentication'])

@router.post('/register')
async def register_user(
    data: UserRequestAdd,
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        try:
            await UsersRepository(session).add(new_user_data)
            await session.commit()
        except :
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'user with email = {data.email} already exists') 

    return {'status': 'OK'}


@router.post('/login')
async def login_user(
    data: UserRequestAdd,
    response: Response
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail='user with this email doesnt exist')
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail='wrong password')
        access_token = AuthService().create_access_token({'user_id': user.id})
        response.set_cookie('access_token', access_token)
        return {'access_token': access_token}


@router.get('/only_auth')
async def only_auth(
    request: Request,
):
    access_token = request.cookies.get('access_token') or None