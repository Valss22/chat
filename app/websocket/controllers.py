from fastapi import APIRouter, Depends
from starlette.websockets import WebSocket

from app.websocket.connection_manager import ConnectionManager
from app.websocket.services import listen_dialog_websocket

websocket_router = APIRouter()


@websocket_router.websocket('/ws/{dialog_id}')
async def websocket_endpoint(
        websocket: WebSocket,
        connection_manager: ConnectionManager = Depends(ConnectionManager)
):
    return await listen_dialog_websocket(websocket, connection_manager)
