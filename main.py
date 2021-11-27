from fastapi import FastAPI

from schemas.user import UserIn, UserOut
from services.user import create_user, auth_user

app = FastAPI()


@app.post('/user/register/', response_model=UserOut)
async def register_user(user: UserIn):
    return await create_user(user)


@app.post('/user/login/', response_model=UserOut)
async def login_user(user: UserIn):
    return await auth_user(user)
