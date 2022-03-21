import pytest
import inspect

from starlette import status
from starlette.responses import JSONResponse

import app
from fastapi import Depends
from starlette.testclient import TestClient
from httpx import AsyncClient
from app.services.dialog import get_dialogs
from app.settings import db
from app.user.controllers import user_router
from unittest.mock import Mock
from app.user.controllers import register_user
from app.user.schemas import UserIn
from app.user.services import UserService


# client = TestClient(user_router)
#
# user_service = UserService()
#
#
class MongoMock:
    class users:

        @staticmethod
        async def insert_one(d: dict):
            return True

        @staticmethod
        async def find_one(d: dict):
            return True


# mongo_mock = MongoMock()
#
#
# @pytest.mark.anyio
# async def test_mocking_constant_a(mocker):
#     mocker.patch.object(app.user.service, 'db', mongo_mock)
#
#     assert JSONResponse(
#         content={'error': 'this user already exists'},
#         status_code=status.HTTP_400_BAD_REQUEST
#     ) == await user_service.create_user(None)


# @pytest.fixture()
# def controller_fixture():
#     def wrapper(
#             user: UserIn,
#             user_service: UserService = Depends(UserService)
#     ):
#         pass
#
#     return wrapper
#
#
# def test_register_controller(controller_fixture):
#     assert inspect.signature(controller_fixture).__str__() == \
#            inspect.signature(register_user).__str__()

#
# async_client = AsyncClient(app=user_router, base_url="http://localhost/")
#
#
# @user_router.get('/')
# async def list_dialogs():
#     return {'ok': '1'}
#     # return await get_dialogs()
#
#
# @pytest.mark.asyncio
# async def test_register_request():
#     async with AsyncClient(app=user_router, base_url="http://localhost/") as ac:
#         response = await ac.get("/")
#     assert response.status_code == 200
