import logging
import pickle
import os
import sys
import argparse


import constants

from vkbottle.bot import Bot
from bps import bps


def create_parser():
    """
    Creates parser for setting bot's token via a cmd argument
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('token', nargs='?', default=os.environ["token"])
    return parser


if __name__ == '__main__':
    """
    Creates parser, checks argument, loads users data and runs the bot
    """
    token_parser = create_parser()
    namespace = token_parser.parse_args(sys.argv[1:])
    token = namespace.token
    try:
        constants.users_info = constants.load_users()
        print("Pickle successful")
    except pickle.UnpicklingError:
        print("UnpicklingError, data won't be loaded")

    bot = Bot(token)
    logging.basicConfig(level=logging.INFO)

    for bp in bps:
        bp.load(bot)

    bot.run_forever()
