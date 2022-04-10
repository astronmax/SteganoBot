from vkbottle.http import AiohttpClient
from vkbottle.bot import Blueprint, Message
from vkbottle.dispatch.rules.base import (FromUserRule)

bp = Blueprint()
http_client = AiohttpClient()


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
    pass


async def audio_message(message: Message):
    """
    Saves user to users_info dictionary
    Tells the url to .mp3 and .ogg to the user

    :param message: Audio message from user
    :return: None
    """
    pass


async def unique_message(message: Message):
    """
    Sees if a received message is a forwarded message
    if the message contains audio messages then it gives a link to
    download it

    :param message: Any message
    :return: None
    """
    pass
