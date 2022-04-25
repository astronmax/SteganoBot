from vkbottle.http import AiohttpClient
from vkbottle.bot import Blueprint, Message

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
    pass


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
    pass


async def unique_message(message: Message):
    """
    Gets text to hide in audio file

    :param message: Any message
    :return: None
    """
    pass
