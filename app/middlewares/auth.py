from typing import Optional
from starlette import status
from starlette.responses import JSONResponse

from app.settings import TOKEN_KEY


# def is_auth(controller):
#     async def wrapper(authorization: Optional[str]):
#         try:
#             token = authorization.split(' ')[1]
#             jwt.decode(token, TOKEN_KEY, algorithms=['HS256'])
#             return await controller(authorization)
#         except jwt.ExpiredSignatureError:
#             return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST)
#
#     return wrapper
