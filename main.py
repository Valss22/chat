from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from schemas.user import UserIn, UserOut, User
from services.user.auth import create_user, auth_user
from services.user.home import get_users

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/user/register/', response_model=UserOut)
async def register_user(user: UserIn):
    return await create_user(user)


@app.post('/user/login/', response_model=UserOut)
async def login_user(user: UserIn):
    return await auth_user(user)


@app.get('/home/', response_model=list[User])
async def list_users():
    return await get_users()
