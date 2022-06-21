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
    def email(self) -> str | None:
        return self.config.get('password_generator', 'email')

    @email.setter
    def email(self, value: str | None):
        if value is not None:
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
    def user_id(self) -> int | None:
        _user_id = self.config.get('telegram', 'user_id')
        if _user_id is not None:
            return int(_user_id)

    @user_id.setter
    def user_id(self, value: str | None):
        if value is not None:
            self.config.set('telegram', 'user_id', value)

    @property
    def token(self) -> str | None:
        return self.config.get('telegram', 'token')

    @token.setter
    def token(self, value: str | None):
        if value is not None:
            self.config.set('telegram', 'token', value)

    @property
    def last_message_id(self) -> int | None:
        _last_message_id = self.config.get('telegram', 'last_message_id')
        if _last_message_id:
            return int(_last_message_id)

    @last_message_id.setter
    def last_message_id(self, value: str | None):
        if value is not None:
            self.config.set('telegram', 'last_message_id', value)

    def save(self):
        with open(self.config_path, 'w') as file:
            self.config.write(file)
