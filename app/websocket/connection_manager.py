from starlette.websockets import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def send_message(self, websocket: WebSocket, message: list[dict]):
        for connection in self.active_connections:
            if id(connection) == id(websocket):
                message[0]['isMine'] = True
            else:
                message[0]['isMine'] = False
            await connection.send_json(message)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
