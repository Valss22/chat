from app.user.model import User
from app.user.schemas import UserIn


class UserService:

    async def create_user(self, user: UserIn):
        if await User.filter(email=user.__dict__['email']):
            return []
        else:
            return [2]
