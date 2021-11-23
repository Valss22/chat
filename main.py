from fastapi import FastAPI, Body
from starlette import status
from starlette.responses import JSONResponse

from schemas.user import UserInSchema, UserOutSchema
from services.user import create_user

app = FastAPI()


@app.post('/user/register')
def register_user(user: UserInSchema):
    return create_user(user)
