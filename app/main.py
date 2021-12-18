from typing import Optional

from fastapi import FastAPI, Header
from starlette.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocket

from app.schemas.dialog import Dialog
from app.schemas.user import UserIn, UserOut
from app.services.dialog import get_dialogs
from app.services.user.auth import create_user, auth_user
from app.services.websocket.dialog import listen_dialog_websocket


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post('/user/register/', response_model=UserOut)
async def register_user(user: UserIn):
    return await create_user(user)


@app.post('/user/login/', response_model=UserOut)
async def login_user(user: UserIn):
    return await auth_user(user)


@app.get('/dialogs/', response_model=list[Dialog])
async def list_dialogs():
    return await get_dialogs()


@app.websocket('/ws/{dialog_id}')
async def websocket_endpoint(websocket: WebSocket):
    return await listen_dialog_websocket(websocket)

