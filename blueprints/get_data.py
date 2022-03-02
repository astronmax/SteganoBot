from constants import users_info
from user import User
import stegano

from vkbottle import DocMessagesUploader
from vkbottle.http import AiohttpClient
from vkbottle.bot import Blueprint, Message

bp = Blueprint()
http_client = AiohttpClient()
hider = stegano.png.TextHider()


@bp.on.message(attachment="doc")
async def attachment_document(message: Message):
    """
    Saves user to users_info dictionary
    If user's state is '1' and user sent a .png file:
        Gets photo as a document and text in the same message
        for hide in the photo
        Encodes text in .png photo and sends it back
        Changes user's state to 0

    If user's state is '2' and user sent a .png file:
        Gets photo as a document
        Decodes text from .png photo and sends it back
        Changes user's state to 0

    Tells the document type, size and url to the user
    :param message: Document message from user
    :return: None
    """
    user_info = await bp.api.users.get(message.from_id)
    user_info = user_info[0]
    if user_info.id not in users_info.keys():
        users_info[user_info.id] = User(user_info.id)

    if users_info[user_info.id].state == 1:
        users_info[user_info.id].active_attachment \
            = message.attachments[0]

    if message.attachments[0].doc.type == 4 and users_info[user_info.id].state == 1:
        doc = await http_client.request_content(message.attachments[0].doc.url)
        with open('image.png', 'wb') as file:
            file.write(doc)
        hider.encode(message.text, 'image.png')
        encoded_doc = await DocMessagesUploader(bp.api).upload(
            "encoded.png", "encoded.png", peer_id=message.peer_id)
        await message.answer("Результат", attachment=encoded_doc)
        users_info[user_info.id].state = 0

    if message.attachments[0].doc.type == 4 and users_info[user_info.id].state == 2:
        doc_get = await http_client.request_content(message.attachments[0].doc.url)
        with open('encoded_got.png', 'wb') as file:
            file.write(doc_get)
        decoded_line = hider.decode('encoded_got.png')
        await message.answer("Результат:")
        await message.answer(decoded_line)
        users_info[user_info.id].state = 0

    await message.answer("Тип документа: {}\nРазмер файла: {} байт\n"
                         "Внутренняя ссылка: {}"
                         .format(message.attachments[0].doc.type,
                                 message.attachments[0].doc.size,
                                 message.attachments[0].doc.url))


@bp.on.message(attachment="audio_message")
async def audio_message(message: Message):
    """
    Saves user to users_info dictionary
    Tells the url to .mp3 and .ogg to the user
    :param message: Audio message from user
    :return: None
    """
    user_info = await bp.api.users.get(message.from_id)
    user_info = user_info[0]
    if user_info.id not in users_info.keys():
        users_info[user_info.id] = User(user_info.id)
    if users_info[user_info.id].state == 2:
        users_info[user_info.id].active_attachment \
            = message.attachments[0]
    await message.answer("Ссылка на mp3: {}\nСсылка на ogg:".format(
        message.attachments[0].audio_message.link_mp3,
        message.attachments[0].audio_message.link_ogg))
