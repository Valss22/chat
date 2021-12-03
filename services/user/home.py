from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from settings import db


class User:
    def __init__(self, **kwargs):
        pass


async def get_users():
    users = await db['users'].find().to_list(50)
    for u in users:
        u['id'] = str(u['_id'])
        del u['_id']
        del u['password']
    return users


# async def get_user(user_id: str):
#     user = await db['users'].find_one({'_id': user_id})
#     return user
