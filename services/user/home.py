from settings import db


async def get_users():
    users = await db['users'].find().to_list(50)
    return users
