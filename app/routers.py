from fastapi import APIRouter

from app.user.controller import user_router

api_router = APIRouter()
api_router.include_router(user_router)
