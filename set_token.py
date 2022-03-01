import os

token = input("Введите токен для записи в Environment ОС\n")
os.environ["token"] = token

print("В Environment ОС записано:\n 'token': '" + os.environ["token"] + "'")
