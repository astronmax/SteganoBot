from constants import users_info
from user import User

from vkbottle.bot import Blueprint, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text

bp = Blueprint()


KEYBOARD = Keyboard(one_time=False, inline=False)
KEYBOARD.add(Text("Зашифровать в фото"), color=KeyboardButtonColor.PRIMARY)
KEYBOARD.add(Text("Зашифровать в голосовом сообщении"),
             color=KeyboardButtonColor.PRIMARY)
KEYBOARD.row()
KEYBOARD.add(Text("Расшифровать фото"), color=KeyboardButtonColor.SECONDARY)
KEYBOARD.add(Text("Расшифровать голосовое сообщение"),
             color=KeyboardButtonColor.SECONDARY)

KEYBOARD = KEYBOARD.get_json()


@bp.on.message(text=["привет<!>", "Привет<!>", "начать<!>", "Начать<!>"])
async def hello_message(message: Message):
    """
    Saves user to users_info dictionary
    Greets user and calls a keyboard for them

    :param message: "привет<!>", "Привет<!>", "начать<!>", "Начать<!>"
    :return: None
    """
    user_info = await bp.api.users.get(message.from_id)
    user_info = user_info[0]
    if user_info.id not in users_info.keys():
        users_info[user_info.id] = User(user_info.id)
    await message.answer("Привет, {}\nДанный бот позволяет зашифровывать "
                         "какую либо информацию в фото и голосовых сообщениях"
                         .format(user_info.first_name))
    await message.answer("Для удобства можете пользоваться клавиатурой",
                         keyboard=KEYBOARD)
    await message.answer("Был создан пользователь " +
                         str(users_info[user_info.id]))
