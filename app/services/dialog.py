from app.settings import db


async def get_dialogs():
    users = await db['users'].find().to_list(50)
    return users
