import os
import sys

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

    If user's state is '4' and user sent file:
        Gets file

        Encodes it to specified user's .wav file

        Sends it back

        Deletes temp files

    If user's state is '5' and user sent file:
        Gets file

        If file format and bytes number in message:
            Decodes file from audio and sends it back

        If bytes number in message:
            Decodes text from audio and sends it back

    Tells the document type, size and url to the user

    :param message: Document message from user
    :return: None
    """
    user_info = await bp.api.users.get(message.from_id)
    user_info = user_info[0]

    clean_image = str(user_info.id) + ".png"
    encoded_image = str(user_info.id) + "_encoded.png"

    if user_info.id not in users_info.keys():
        users_info[user_info.id] = User(user_info.id)

    if users_info[user_info.id].state == 1:
        users_info[user_info.id].active_attachment \
            = message.attachments[0]

    if message.attachments[0].doc.type == 4 \
            and users_info[user_info.id].state == 1:
        doc = await http_client.request_content(message.attachments[0].doc.url)

        with open(clean_image, 'wb') as file:
            file.write(doc)
        hider.encode(message.text, clean_image, encoded_image)

        encoded_doc = await DocMessagesUploader(bp.api).upload(
            encoded_image, encoded_image, peer_id=message.peer_id)
        await message.answer("Результат", attachment=encoded_doc)
        users_info[user_info.id].state = 0
        os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               clean_image))
        os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               encoded_image))

    if message.attachments[0].doc.type == 4 \
            and users_info[user_info.id].state == 2:
        doc_get = \
            await http_client.request_content(message.attachments[0].doc.url)
        with open(encoded_image, 'wb') as file:
            file.write(doc_get)
        decoded_line = hider.decode(encoded_image)
        await message.answer("Результат:")
        await message.answer(decoded_line)
        users_info[user_info.id].state = 0
        os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               encoded_image))

    if users_info[user_info.id].state == 4:
        if message.text == "" and message.attachments:
            input_wav = str(user_info.id) + ".wav"
            hidden = str(user_info.id) + "_hidden.md"
            file_in_bytes = await http_client. \
                request_content(message.attachments[0].doc.url)

            stegano.wav.hide_bytes(input_wav, file_in_bytes, hidden, 3)
            uploaded_hidden = await DocMessagesUploader(bp.api).upload(
                hidden, hidden, peer_id=message.peer_id)
            await message.answer("Зашифрованый файл в формате .md\n"
                                 "Поменяйте формат файла на .wav чтобы его "
                                 "прослушать",
                                 attachment=uploaded_hidden)
            await message.answer("Обязательно запомните формат файла и число "
                                 "байтов, равное: " +
                                 str(sys.getsizeof(file_in_bytes)))
            os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                   input_wav))
            os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                   hidden))

    if users_info[user_info.id].state == 5:
        doc_get = \
            await http_client.request_content(message.attachments[0].doc.url)
        hidden_name = str(user_info.id) + "_hidden.wav"
        with open(hidden_name, 'wb') as file:
            file.write(doc_get)
        if ":" in message.text:
            file_format = str(user_info.id) + message.text.split(":")[0]
            byte_number = int(message.text.split(":")[1])
            stegano.wav.recover_data(hidden_name, file_format, 3, byte_number)

            decoded = await DocMessagesUploader(bp.api).upload(
                file_format, file_format, peer_id=message.peer_id)
            await message.answer("Расшифрованный файл: ", attachment=decoded)
            os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                   file_format))
        else:
            encoded = stegano.wav.recover_data(hidden_name,
                                               "", 2, int(message.text))
            decoded = encoded.decode()
            await message.answer("Расшифрованное сообщение:")
            await message.answer(decoded)
        os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               hidden_name))

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

    Gets mp3, converts it to .wav, sends .md version of sent audio message
    back

    Changes state to 4

    :param message: Audio message from user
    :return: None
    """
    user_info = await bp.api.users.get(message.from_id)
    user_info = user_info[0]

    mp3_name = str(user_info.id) + ".mp3"
    wav_name = str(user_info.id) + ".wav"
    md_name = str(user_info.id) + ".md"
    try:
        os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               mp3_name))
    except:
        print("No data erased")

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

        with open(mp3_name, 'wb') as file:
            file.write(audio)
        convert.convert_mp3_to_wav(mp3_name, md_name)

        converted = await DocMessagesUploader(bp.api).upload(
            md_name, md_name, peer_id=message.peer_id)
        await message.answer("Ваше голосовое в формате .md, так как в VK "
                             "нельзя отправлять .wav файлы",
                             attachment=converted)
        os.rename(md_name, wav_name)
        await message.answer("Вы можете спрятать данные размером до: " +
                             str(stegano.wav.get_size_to_hide(wav_name, 3)) +
                             " байтов")

        users_info[user_info.id].state = 4
        os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                               mp3_name))


@bp.on.message(FromUserRule())
async def unique_message(message: Message):
    """
    Gets text to hide in audio file

    :param message: Any message
    :return: None
    """
    user_info = await bp.api.users.get(message.from_id)
    user_info = user_info[0]

    if users_info[user_info.id].state == 4:
        if message.text:
            input_wav = str(user_info.id) + ".wav"
            hidden = str(user_info.id) + "_hidden.md"
            text_in_bytes = message.text.encode()

            stegano.wav.hide_bytes(input_wav, text_in_bytes, hidden, 3)
            uploaded_hidden = await DocMessagesUploader(bp.api).upload(
                hidden, hidden, peer_id=message.peer_id)
            await message.answer("Зашифрованый файл в формате .md\n"
                                 "Поменяйте формат файла на .wav чтобы его "
                                 "прослушать",
                                 attachment=uploaded_hidden)
            await message.answer("Обязательно запомните формат файла и число "
                                 "байтов, равное: " +
                                 str(sys.getsizeof(text_in_bytes)))
            os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                   input_wav))
            os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                   hidden))
