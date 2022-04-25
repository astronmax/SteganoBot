from vkbottle.bot import Blueprint, Message

bp = Blueprint()


async def decrypt_photo(message: Message):
    """
    Saves user to users_info dictionary
    Changes user state to 2
    Pickles users_info dictionary

    :param message: "Расшифровать фото"
    :return: None
    """
    pass


async def decrypt_audio(message: Message):
    """
    Saves user to users_info dictionary
    Changes user state to 5
    Pickles users_info dictionary

    :param message: "Расшифровать аудио"
    :return: None
    """
    pass