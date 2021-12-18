from typing import Optional, Final

from bson import ObjectId
from starlette.websockets import WebSocket

from app.services.dialog import get_interlocutor_id
from app.services.user.auth import get_current_user_id
from app.settings import db

COUNT_INITIAL_MESSAGES: Final[int] = 20

SENDER: Final[str] = 'sender'
RECEIVER: Final[str] = 'receiver'


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


async def listen_dialog_websocket(
        websocket: WebSocket
):
    await websocket.accept()
    users_id: dict = await websocket.receive_json()

    current_user_id: str = users_id['current']
    interlocutor_id: str = users_id['interlocutor']

    dialog_service = WebsocketDialogService(
        current_user_id, interlocutor_id
    )
    messages = await dialog_service.get_messages(current_user_id)
    await websocket.send_json(messages)

    while True:
        message_data: dict = await websocket.receive_json()
        text: str = message_data['text']
        sender_id: str = message_data['senderId']
        message_id = ObjectId()
        dialog_service.save_message(text, message_id)
        if sender_id == current_user_id:
            is_mine = True
        else:
            is_mine = False
        await websocket.send_json([
            {'_id': str(message_id),
             'text': text, 'isMine': is_mine}
        ])
