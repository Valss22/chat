from app.settings import db


async def get_dialogs():
    users = await db['users'].find().to_list(50)
    return users


def get_interlocutor_id(dialog_id: str, current_user_id: str) -> str:
    dialog_id_ords: list[int] = [int(i) for i in dialog_id.split('&')]
    current_user_ords: list[int] = [ord(i) for i in current_user_id]
    interlocutor_id_ords: list = []

    for i in range(len(current_user_id)):
        a = dialog_id_ords[i]
        b = current_user_ords[i]
        interlocutor_id_ords.append((a + b))

    interlocutor_id_chrs: list = [chr(i) for i in interlocutor_id_ords]
    interlocutor_id: str = ''.join(interlocutor_id_chrs)
    return interlocutor_id

