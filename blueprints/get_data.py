from constants import users_info

from vkbottle.bot import Blueprint, Message

bp = Blueprint()


@bp.on.message(attachment="doc")
async def attachment_document(message: Message):
    user_info = await bp.api.users.get(message.from_id)
    user_info = user_info[0]
    if users_info[user_info.id].state == 1:
        users_info[user_info.id].active_attachment \
            = message.attachments[0]
    await message.answer("Тип документа: {}\nРазмер файла: {} байт\n"
                         "Внутренняя ссылка: {}"
                         .format(message.attachments[0].doc.type,
                                 message.attachments[0].doc.size,
                                 message.attachments[0].doc.url))
