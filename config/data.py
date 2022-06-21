"""Module for managing dynamic app data"""

import configparser
import pathlib
import os


class PasswordGeneratorData:
    """Data for the whole project"""

    config = configparser.ConfigParser()
    config_path = pathlib.Path(os.curdir) / 'config.ini'
    config.read(config_path)

    @property
    def email(self):
        return self.config.get('password_generator', 'email')

    @email.setter
    def email(self, value):
        self.config.set('password_generator', 'email', value)

    def save(self):
        with open(self.config_path, 'w') as file:
            self.config.write(file)


class TelegramData:
    """Data for work with telegram"""

    config = configparser.ConfigParser()
    config_path = pathlib.Path(os.curdir) / 'config.ini'
    config.read(config_path)

    @property
    def user_id(self) -> int:
        return int(self.config.get('telegram', 'user_id'))

    @user_id.setter
    def user_id(self, value: str):
        self.config.set('telegram', 'user_id', value)

    @property
    def token(self) -> str:
        return self.config.get('telegram', 'token')

    @token.setter
    def token(self, value: str):
        self.config.set('telegram', 'token', value)

    @property
    def last_message_id(self) -> int:
        return int(self.config.get('telegram', 'last_message_id'))

    @last_message_id.setter
    def last_message_id(self, value: str):
        self.config.set('telegram', 'last_message_id', value)

    def save(self):
        with open(self.config_path, 'w') as file:
            self.config.write(file)
