from starlette.websockets import WebSocket

from app.services.websocket.connection_manager import ConnectionManager


class WebsocketDialogService(ConnectionManager):
    pass


async def listen_dialog_websocket(websocket: WebSocket, user_id: str):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data} and user id {user_id}")
