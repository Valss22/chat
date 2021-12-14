from typing import Optional

from starlette.websockets import WebSocket

from app.services.user.auth import get_current_user_id
from app.settings import db

from app.services.websocket.connection_manager import ConnectionManager


class WebsocketDialogService(ConnectionManager):
    pass


async def listen_dialog_websocket(
        websocket: WebSocket, user_id: str,
        Authorization: Optional[str]
):
    await websocket.accept()
    current_user_id: str = await get_current_user_id(Authorization)
    users: list[str] = [current_user_id, user_id]
    await db['messages'].insert_one({'users': users})
    while True:
        data = await websocket.receive_text()
        db['messages'].find_one({'users': users}).update({'text': data})
        await websocket.send_text(f"Message text was: {data} and user id {user_id}")
