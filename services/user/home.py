from settings import db


async def get_users():
    users = await db['users'].find().to_list(50)
    return users
#
#
# async def get_user(user_id: str):
#     user = await db['users'].find_one({'_id': user_id})
#     return user
