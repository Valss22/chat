from time import time

import bcrypt
import jwt
from starlette import status
from starlette.responses import JSONResponse

from app.schemas.user import UserIn
from app.settings import db, TOKEN_KEY, SALT

TOKEN_TIME = 40_000


def get_payload(username: str) -> dict:
    return {
        'username': username,
        'exp': time() + TOKEN_TIME
    }


async def create_user(user: UserIn):
    username: str = user.dict()['username']

    if await db['users'].find_one({'username': username}):
        return JSONResponse(
            content={'error': 'this user already exists'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    user.__dict__['password'] = bcrypt.hashpw(
        user.dict()['password'].encode(), SALT
    )
    created_user = await db['users'].insert_one(user.dict())
    payload = get_payload(username)
    user.__dict__['token'] = jwt.encode(payload, TOKEN_KEY)
    user.__dict__['_id'] = created_user.inserted_id
    return user


async def auth_user(user: UserIn):
    username: str = user.dict()['username']
    password: bytes = user.dict()['password'].encode()
    current_user = await db['users'].find_one({'username': username})

    if current_user:
        hashed_password: bytes = current_user['password']
        if bcrypt.checkpw(password, hashed_password):
            payload = get_payload(username)
            user.__dict__['token'] = jwt.encode(payload, TOKEN_KEY)
            user.__dict__['_id'] = current_user['_id']
            return user
        return JSONResponse(
            content={'error': 'Auth failed'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    return JSONResponse(
        content={'error': 'User does not exists'},
        status_code=status.HTTP_400_BAD_REQUEST
    )
