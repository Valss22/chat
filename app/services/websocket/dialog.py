from typing import Final, Optional

from bson import ObjectId
from fastapi import Header
from starlette.websockets import WebSocket, WebSocketDisconnect

from app.services.user.auth import get_current_user_id
from app.services.websocket.connection_manager import ConnectionManager
from app.settings import db

COUNT_INITIAL_MESSAGES: Final[int] = 20


class WebsocketDialogService:

    def __init__(self, current_user_id: str, interlocutor_id: str):
        self.users: dict[str, str] = {
            'sender': current_user_id,
            'receiver': interlocutor_id,
        }

    def save_message(self, text: str, message_id: ObjectId) -> None:
        db['messages'].insert_one({
            '_id': message_id, 'users': self.users,
            'text': text,
        })

    async def get_messages(self, current_user_id: str) -> list[dict]:
        reversed_users = {
            'sender': self.users['receiver'],
            'receiver': self.users['sender']
        }
        messages = db['messages'].find(
            {'$or': [{'users': self.users},
                     {'users': reversed_users}]}
        ).sort('_id')
        messages = await messages.to_list(COUNT_INITIAL_MESSAGES)

        for msg in messages:
            msg['_id'] = str(msg['_id'])
            if current_user_id == msg['users']['sender']:
                msg['isMine'] = True
            else:
                msg['isMine'] = False
            del msg['users']
        return messages


manager = ConnectionManager()


async def listen_dialog_websocket(
        websocket: WebSocket
):
    await manager.connect(websocket)

    users_id: dict = await websocket.receive_json()

    current_user_id: str = users_id['current']
    interlocutor_id: str = users_id['interlocutor']

    dialog = WebsocketDialogService(
        current_user_id, interlocutor_id
    )
    messages = await dialog.get_messages(current_user_id)
    await websocket.send_json(messages)

    try:
        while True:
            text: str = await websocket.receive_text()
            message_id = ObjectId()
            dialog.save_message(text, message_id)
            await manager.send_message(websocket, [
                {'_id': str(message_id),
                 'text': text, 'isMine': None}
            ])
    except WebSocketDisconnect:
        manager.disconnect(websocket)
