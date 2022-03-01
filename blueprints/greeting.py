from constants import users_info
from user import User

from vkbottle.bot import Blueprint, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text

bp = Blueprint()

KEYBOARD = Keyboard(one_time=True, inline=False)
KEYBOARD.add(Text("Подсказка"), color=KeyboardButtonColor.POSITIVE)
KEYBOARD.row()
KEYBOARD.add(Text("Зашифровать в фото"), color=KeyboardButtonColor.PRIMARY)
KEYBOARD.add(Text("Зашифровать в голосовом сообщении"),
             color=KeyboardButtonColor.SECONDARY)
KEYBOARD = KEYBOARD.get_json()


@bp.on.message(text=["привет<!>", "Привет<!>", "начать<!>", "Начать<!>"])
async def hello_message(message: Message):
    user_info = await bp.api.users.get(message.from_id)
    user_info = user_info[0]
    print(user_info)
    if user_info.id not in users_info.keys():
        users_info[user_info.id] = User(user_info.id)
    await message.answer("Привет, {}\nДанный бот позволяет зашифровывать "
                         "какую либо информацию в фото и голосовых сообщениях"
                         .format(user_info.first_name))
    await message.answer("Для удобства можете пользоваться клавиатурой",
                         keyboard=KEYBOARD)
    await message.answer("Был создан пользователь " +
                         str(users_info[user_info.id]))
