from vkbottle.bot import Blueprint, Message

bp = Blueprint()


async def encrypt_photo(message: Message):
    """
    Saves user to users_info dictionary
    Changes user state to 1
    Allows user to send photo as a document and
    write text to hide in the photo in the next message

    :param message: "Зашифровать в фото"
    :return: None
    """
    pass


async def encrypt_audio_message(message: Message):
    """
    Saves user to users_info dictionary
    Changes user state to 3
    Allows user to send photo as a document and
    write text to hide in the photo in the next message

    :param message: "Зашифровать в голосовом сообщении"
    :return: None
    """
    pass
