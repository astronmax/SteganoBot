# SteganoBot
## Bot for hiding information in images
This is a bot in social network [VK](https://vk.com/).
It uses [Vkbottle](https://github.com/vkbottle/vkbottle) framework, [Numpy](https://github.com/numpy/numpy) and [Pillow](https://github.com/python-pillow/Pillow).

Using buttons in direct messages with this bot, you can opperate with various tools to **encode** and **decode** the desired text in png format image.

The project is under development,so in the future it is planned to release processing with:
* GIF image format 
* BMP
* RAW

Moreover, there is also an idea to add an ability of encoding and decoding information in audio-format files, such as 
* WAV 
* AIFF

To start the program in local regime and test it, you can run **<format_name>_local_test.py** file, for example png_local_test.py.

To start the bot, simply use: **python main.py TOKEN**, where TOKEN is your vk-bot token or **python main.py**, if you have the token set in your PATH/Environment. 

It is planned to work on an ongoing basis on web server [Heroku](https://www.heroku.com/), so VK users could use this bot whenever they want.

