from time import time

import bcrypt
import jwt
from starlette import status
from starlette.responses import JSONResponse

from schemas.user import UserIn
from settings import db, TOKEN_KEY, SALT

TOKEN_TIME = 40_000


def get_payload(username: str) -> dict:
    return {
        'username': username,
        'exp': time() + TOKEN_TIME
    }


async def create_user(user: UserIn):
    username: str = user.__dict__['username']
    if await db['users'].find_one({'username': username}):
        return JSONResponse(
            content={'error': 'this user already exists'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    user.__dict__['password'] = bcrypt.hashpw(
        user.__dict__['password'].encode(), SALT
    )
    new_user = await db['users'].insert_one(user.__dict__)
    user.__dict__['id'] = str(new_user.inserted_id)
    payload = get_payload(username)
    user.__dict__['token'] = jwt.encode(payload, TOKEN_KEY)
    return user


async def auth_user(user: UserIn):
    username: str = user.__dict__['username']
    password: bytes = user.__dict__['password'].encode()
    current_user = await db['users'].find_one({'username': username})

    if current_user:
        hashed_password: bytes = current_user['password']
        if bcrypt.checkpw(password, hashed_password):
            user.__dict__['id'] = str(current_user['_id'])
            payload = get_payload(username)
            user.__dict__['token'] = jwt.encode(payload, TOKEN_KEY)
            return user
        return JSONResponse(
            content={'error': 'Auth failed'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    return JSONResponse(
        content={'error': 'User does not exists'},
        status_code=status.HTTP_400_BAD_REQUEST
    )
