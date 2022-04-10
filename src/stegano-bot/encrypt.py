from constants import users_info
from user import User

from vkbottle.bot import Blueprint, Message

bp = Blueprint()


@bp.on.message(text="Зашифровать в фото")
async def encrypt_photo(message: Message):
    """
    Saves user to users_info dictionary
    Changes user state to 1
    Allows user to send photo as a document and
    write text to hide in the photo in the next message

    :param message: "Зашифровать в фото"
    :return: None
    """
    user_info = await bp.api.users.get(message.from_id)
    user_info = user_info[0]
    if user_info.id not in users_info.keys():
        users_info[user_info.id] = User(user_info.id)
    users_info[user_info.id].state = 1
    await message.answer("Загрузите фото и напишите в этом же сообщении текст "
                         "для шифрования в фото")
    await message.answer("State у " + str(user_info.id) + " был изменён на "
                         + str(users_info[user_info.id].state))


@bp.on.message(text="Зашифровать в голосовом сообщении")
async def encrypt_audio_message(message: Message):
    """
    Saves user to users_info dictionary
    Changes user state to 3
    Allows user to send photo as a document and
    write text to hide in the photo in the next message

    :param message: "Зашифровать в голосовом сообщении"
    :return: None
    """
    user_info = await bp.api.users.get(message.from_id)
    user_info = user_info[0]
    if user_info.id not in users_info.keys():
        users_info[user_info.id] = User(user_info.id)
    users_info[user_info.id].state = 3
    await message.answer("Запишите голосовое сообщение "
                         "и в следующем сообщении напишите текст "
                         "для шифрования в фото")
    await message.answer("State у " + str(user_info.id) + " был изменён на "
                         + str(users_info[user_info.id].state))
