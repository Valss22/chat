from fastapi import APIRouter, Depends

from app.user.schemas import UserIn
from app.user.service import UserService

user_router = APIRouter(
    prefix='/user'
)


@user_router.post('/register/')
async def register_user(user: UserIn, user_service: UserService = Depends()):
    return await user_service.create_user(user)
