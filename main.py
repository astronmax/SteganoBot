import logging
import pickle

import constants

from vkbottle.bot import Bot
from blueprints import bps

try:
    constants.users_info = constants.load_users()
    print("Pickle successful")
except pickle.UnpicklingError:
    print("UnpicklingError, data won't be loaded")

bot = Bot("29e2bdd91405a6cb1f2d35bc02edf0d089725d24a38f2c5de"
          "ba73eaa8cb6a6e4ca6b589485940fbb1240c")
logging.basicConfig(level=logging.INFO)

for bp in bps:
    bp.load(bot)

bot.run_forever()
