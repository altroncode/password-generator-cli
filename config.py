import configparser
import os
import pathlib


config = configparser.ConfigParser()
config_path = pathlib.Path(os.curdir) / 'config.ini'
config.read(config_path)


class PasswordGeneratorSettings:
    email = config.get('password_generator', 'email')


class TelegramSettings:
    user_id = int(config.get('telegram', 'user_id'))
    token = config.get('telegram', 'tg_bot_token')
    message_id = int(config.get('telegram', 'last_message_id'))

