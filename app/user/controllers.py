from fastapi import APIRouter, Depends

from app.user.schemas import UserOut, UserIn
from app.user.services import UserService

user_router = APIRouter()


@user_router.post('/user/register/', response_model=UserOut)
async def register_user(user: UserIn, user_service: UserService = Depends(UserService)):
    return await user_service.create_user(user)


@user_router.post('/user/login/', response_model=UserOut)
async def login_user(user: UserIn, user_service: UserService = Depends(UserService)):
    return await user_service.auth_user(user)
