from fastapi import APIRouter, HTTPException, Response, Request, status

from src.repositories.users import UsersRepository
from src.database import async_session_maker
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep, DBDep


router = APIRouter(prefix='/auth', tags=['Autherization and authentication'])


@router.post('/register')
async def register_user(
    data: UserRequestAdd,
    db: DBDep
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    await db.users.add(new_user_data)
    await db.commit()

    return {'status': 'OK'}


@router.post('/login')
async def login_user(
    data: UserRequestAdd,
    response: Response,
    db: DBDep
):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(status_code=401, detail='user not found')
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='incorrect password')
    access_token = AuthService().create_access_token({'user_id': user.id})
    response.set_cookie('access_token', access_token)
    return {'access_token': access_token}


@router.get('/me')
async def get_me(
    user_id: UserIdDep,
    db: DBDep
):
    user = await db.users.get_one_or_none(id=user_id)
    return user


@router.get('/only_auth')
async def only_auth(
    request: Request,
    user_id: UserIdDep
):
    access_token = request.cookies.get('access_token')
    data = AuthService().decode_token(access_token)
    user_id = data.get('user_id')
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user


@router.get('/logout')
async def logout(
    response: Response
):
    response.delete_cookie('access_token')
    return {'status': 'OK'}