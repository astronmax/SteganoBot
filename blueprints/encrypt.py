from constants import users_info

from vkbottle.bot import Blueprint, Message

bp = Blueprint()


@bp.on.message(text="Зашифровать в фото")
async def encrypt_photo(message: Message):
    user_info = await bp.api.users.get(message.from_id)
    user_info = user_info[0]
    users_info[user_info.id].state = 1
    await message.answer("Загрузите фото и напишите в этом же сообщении текст "
                         "для шифрования в фото")
    await message.answer("State у " + str(user_info.id) + " был изменён на "
                         + str(users_info[user_info.id].state))
