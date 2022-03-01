import logging

from vkbottle.bot import Bot
from blueprints import bps

bot = Bot("29e2bdd91405a6cb1f2d35bc02edf0d089725d24a38f2c5de"
          "ba73eaa8cb6a6e4ca6b589485940fbb1240c")
logging.basicConfig(level=logging.INFO)

for bp in bps:
    bp.load(bot)

bot.run_forever()
