from typing import Optional

import jwt
from starlette import status
from starlette.responses import JSONResponse

from app.settings import TOKEN_KEY


def is_auth(controller):
    async def wrapper(Authorization: Optional[str]):
        try:
            token = Authorization.split(' ')[1]
            jwt.decode(token, TOKEN_KEY, algorithms='HS256')
            return await controller(Authorization)
        except jwt.ExpiredSignatureError:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST)

    return wrapper
