"""Module for managing dynamic app data"""

import configparser
import os
import pathlib


config = configparser.ConfigParser()
config_path = pathlib.Path(os.curdir) / 'config.ini'
config.read(config_path)


class PasswordGeneratorData:
    """Data for the whole project"""

    email = config.get('password_generator', 'email')


class TelegramData:
    """Data for work with telegram"""

    user_id = int(config.get('telegram', 'user_id'))
    token = config.get('telegram', 'token')
    last_message_id = int(config.get('telegram', 'last_message_id'))
