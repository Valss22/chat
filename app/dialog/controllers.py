from fastapi import APIRouter, Depends

from app.dialog.services import DialogService

dialog_router = APIRouter()


@dialog_router.get('/dialogs/')
async def list_dialogs(dialog_service: DialogService = Depends(DialogService)):
    return await dialog_service.get_dialogs(50)
