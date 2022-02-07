from time import time
from typing import Optional, Union

import bcrypt
import jwt
from starlette import status
from starlette.responses import JSONResponse

from app.user.schemas import UserIn
from app.settings import db, TOKEN_KEY, SALT

TOKEN_TIME = 40_000


def get_payload(user_id: str) -> dict:
    return {
        '_id': user_id,
        'exp': time() + TOKEN_TIME
    }


async def get_current_user_id(Authorization: Optional[str]) -> Optional[str]:
    if Authorization:
        token = Authorization.split(' ')[1]
        decoded_token: dict = jwt.decode(
            token, TOKEN_KEY, algorithms='HS256'
        )
        return str(decoded_token['_id'])
    raise ValueError


class UserService:

    async def create_user(self, user: UserIn) -> Union[UserIn, JSONResponse]:
        username: str = user.dict()['username']

        if await db.users.find_one({'username': username}):
            return JSONResponse(
                content={'error': 'this user already exists'},
                status_code=status.HTTP_400_BAD_REQUEST
            )
        user.__dict__['password'] = bcrypt.hashpw(
            user.dict()['password'].encode(), SALT
        )
        created_user = await db.users.insert_one(user.dict())
        payload = get_payload(str(created_user.inserted_id))
        user.__dict__['token'] = jwt.encode(payload, TOKEN_KEY)
        user.__dict__['_id'] = created_user.inserted_id
        return user

    async def auth_user(self, user: UserIn) -> Union[UserIn, JSONResponse]:
        username: str = user.dict()['username']
        password: bytes = user.dict()['password'].encode()
        current_user = await db['users'].find_one({'username': username})

        if current_user:
            hashed_password: bytes = current_user['password']
            if bcrypt.checkpw(password, hashed_password):
                payload = get_payload(str(current_user['_id']))
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
