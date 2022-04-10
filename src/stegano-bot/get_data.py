import os
from constants import users_info
from user import User
import stegano
from soundTasks import convert

from vkbottle import DocMessagesUploader
from vkbottle.http import AiohttpClient
from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import (FromUserRule)

bp = Blueprint()
http_client = AiohttpClient()
hider = stegano.png.TextHider()


@bp.on.message(attachment="doc")
async def attachment_document(message: Message):
    """
    Saves user to users_info dictionary
    If user's state is '1' and user sent a .png file:
        Gets photo as a document and text in the same message
        for hiding in the photo

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

    if message.attachments[0].doc.type == 4 \
            and users_info[user_info.id].state == 1:
        doc = await http_client.request_content(message.attachments[0].doc.url)
        with open('image.png', 'wb') as file:
            file.write(doc)
        hider.encode(message.text, 'image.png')
        encoded_doc = await DocMessagesUploader(bp.api).upload(
            "encoded.png", "encoded.png", peer_id=message.peer_id)
        await message.answer("Результат", attachment=encoded_doc)
        users_info[user_info.id].state = 0
        os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               'image.png'))

    if message.attachments[0].doc.type == 4 \
            and users_info[user_info.id].state == 2:
        doc_get = \
            await http_client.request_content(message.attachments[0].doc.url)
        with open('encoded_got.png', 'wb') as file:
            file.write(doc_get)
        decoded_line = hider.decode('encoded_got.png')
        await message.answer("Результат:")
        await message.answer(decoded_line)
        users_info[user_info.id].state = 0
        os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               'encoded_got.png'))

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

    await message.answer("Ссылка на mp3: {}\nСсылка на ogg:".format(
        message.attachments[0].audio_message.link_mp3,
        message.attachments[0].audio_message.link_ogg))

    if users_info[user_info.id].state == 3:
        users_info[user_info.id].active_attachment \
            = message.attachments[0]

        audio = await http_client.request_content(message.attachments[0]
                                                  .audio_message.link_mp3)
        with open('audioMessage.mp3', 'wb') as file:
            file.write(audio)
        convert.convert_mp3_to_wav("audioMessage.mp3", "out.wav")
        converted = await DocMessagesUploader(bp.api).upload(
            "out.wav", "out.wav", peer_id=message.peer_id)
        await message.answer("Ваше голосовое в формате .wav",
                             attachment=converted)

        users_info[user_info.id].state = 4
        os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               'audioMessage.mp3'))


@bp.on.message(FromUserRule())
async def unique_message(message: Message):
    """
    Sees if a received message is a forwarded message
    if the message contains audio messages then it gives a link to
    download it

    :param message: Any message
    :return: None
    """
    user_info = await bp.api.users.get(message.from_id)
    user_info = user_info[0]
    if users_info[user_info.id].state == 4:
        print(message.text)
    if message.fwd_messages[0]:
        await message.answer(str(message.fwd_messages[0].attachments[0]
                                 .audio_message.link_mp3))
        await message.answer(str(message.fwd_messages[0].attachments[0]
                                 .audio_message.link_ogg))
