from constants import users_info, save_users
from user import User

from vkbottle.bot import Blueprint, Message

bp = Blueprint()


@bp.on.message(text="Расшифровать фото")
async def decrypt_photo(message: Message):
    """
    Saves user to users_info dictionary
    Changes user state to 2
    Pickles users_info dictionary

    :param message: "Расшифровать фото"
    :return: None
    """
    user_info = await bp.api.users.get(message.from_id)
    user_info = user_info[0]
    if user_info.id not in users_info.keys():
        users_info[user_info.id] = User(user_info.id)
    users_info[user_info.id].state = 2
    await message.answer("Загрузите фото в следующем сообщении")
    await save_users(users_info)


@bp.on.message(text="Расшифровать аудио")
async def decrypt_audio(message: Message):
    """
    Saves user to users_info dictionary
    Changes user state to 5
    Pickles users_info dictionary

    :param message: "Расшифровать аудио"
    :return: None
    """
    user_info = await bp.api.users.get(message.from_id)
    user_info = user_info[0]
    if user_info.id not in users_info.keys():
        users_info[user_info.id] = User(user_info.id)
    users_info[user_info.id].state = 5
    await message.answer("Загрузите файл в формате .md в следующем сообщении\n"
                         "И напишите сообщение в виде:\n"
                         "'.ФОРМАТ:КОЛИЧЕСТВО_БАЙТОВ' - если зашифрован файл\n"
                         "'КОЛИЧЕСТВО_БАЙТОВ' - если зашифрован текст ВК")
    await save_users(users_info)
