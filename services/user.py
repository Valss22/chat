from schemas.user import UserInSchema
from settings import db


def create_user(user: UserInSchema):
    db['users'].insert_one(user.__dict__)
    return {'message': 'ok!'}
