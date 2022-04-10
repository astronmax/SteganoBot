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
    await message.answer("State у " + str(user_info.id) + " был изменён на "
                         + str(users_info[user_info.id].state))
    await save_users(users_info)
