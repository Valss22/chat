from app.settings import db


class DialogService:

    async def get_dialogs(self, count: int):
        users = await db['users'].find().to_list(count)
        return users
