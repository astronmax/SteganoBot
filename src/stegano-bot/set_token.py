import os


def set_token():
    """
    Asks for your VK bot's token in order to write it to PATH/Environment of
    your system
    """
    token = input("Введите токен для записи в Environment ОС\n")
    os.environ["token"] = token

    print("В Environment ОС записано:\n 'token': '" + os.environ["token"] + "'")
