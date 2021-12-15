from typing import Optional, Final
from pydantic import parse_obj_as
from starlette.websockets import WebSocket

from app.schemas.message import Message
from app.services.user.auth import get_current_user_id
from app.settings import db

COUNT_INITIAL_MESSAGES: Final[int] = 20

SENDER: Final[str] = 'sender'
RECEIVER: Final[str] = 'receiver'


class WebsocketDialogService:

    def __init__(self, current_user_id: str, user_id: str):
        self.users: dict[str, str] = {
            'sender': current_user_id,
            'receiver': user_id,
        }

    def save_message(self, text: str, sender_or_receiver: str) -> None:
        if sender_or_receiver == SENDER:
            is_mine = True
        else:
            is_mine = False
        db['messages'].insert_one({
            'users': self.users, 'text': text,
            'is_mine': is_mine
        })

    async def get_messages(self) -> list[dict]:
        messages = db['messages'].find({'users': self.users}).sort('_id', -1)
        messages = await messages.to_list(COUNT_INITIAL_MESSAGES)
        # parsed_messages = parse_obj_as(list[Message], messages)
        return messages


async def listen_dialog_websocket(
        websocket: WebSocket, user_id: str,
        Authorization: Optional[str]
):
    await websocket.accept()
    current_user_id: str = await get_current_user_id(Authorization)
    dialog_service = WebsocketDialogService(current_user_id, user_id)
    messages = await dialog_service.get_messages()
    await websocket.send_json(messages)

    while True:
        text: str = await websocket.receive_text()
        dialog_service.save_message(text, RECEIVER)
        await dialog_service.get_messages()
        # await websocket.send_text(f"Message text was: {text} and user id {user_id}")
