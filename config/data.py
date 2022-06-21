"""Module for managing dynamic app data"""

import configparser
import os
import pathlib


class PasswordGeneratorData:
    """Data for the whole project"""

    config = configparser.ConfigParser()
    config_path = pathlib.Path(os.curdir) / 'config.ini'
    config.read(config_path)

    def __init__(self):
        self.email = self.config.get('password_generator', 'email')


class TelegramData:
    """Data for work with telegram"""

    config = configparser.ConfigParser()
    config_path = pathlib.Path(os.curdir) / 'config.ini'
    config.read(config_path)

    def __init__(self):
        self.user_id = int(self.config.get('telegram', 'user_id'))
        self.token = self.config.get('telegram', 'token')
        self.last_message_id = int(self.config.get('telegram', 'last_message_id'))
