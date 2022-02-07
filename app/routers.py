from fastapi import APIRouter

from app.dialog.controllers import dialog_router
from app.user.controllers import user_router
from app.websocket.controllers import websocket_router

api_router = APIRouter()

api_router.include_router(user_router)
api_router.include_router(dialog_router)
api_router.include_router(websocket_router)
