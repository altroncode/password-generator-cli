"""Module for setting project"""

import configparser
import pathlib
import os


class PasswordSettings:
    config = configparser.ConfigParser()
    config_path = pathlib.Path(os.curdir) / 'settings.ini'
    config.read(config_path)

    @property
    def default_length(self) -> str | None:
        return self.config.get('password', 'default_length')

    @default_length.setter
    def default_length(self, value: str | None):
        if value is not None:
            self.config.set('password', 'default_length', value)

    @property
    def digits_in_password(self) -> str | None:
        return self.config.get('password', 'digits_in_password')

    @digits_in_password.setter
    def digits_in_password(self, value: str | None):
        if value is not None:
            self.config.set('password', 'digits_in_password', value)

    @property
    def capital_letters_in_password(self) -> str | None:
        return self.config.get('password', 'capital_letters_in_password')

    @capital_letters_in_password.setter
    def capital_letters_in_password(self, value: str | None):
        if value is not None:
            self.config.set('password', 'capital_letters_in_password', value)

    @property
    def small_letters_in_password(self) -> str | None:
        return self.config.get('password', 'small_letters_in_password')

    @small_letters_in_password.setter
    def small_letters_in_password(self, value: str | None):
        if value is not None:
            self.config.set('password', 'small_letters_in_password', value)

    @property
    def punctuation_in_password(self) -> str | None | None:
        return self.config.get('password', 'punctuation_in_password')

    @punctuation_in_password.setter
    def punctuation_in_password(self, value: str | None):
        if value is not None:
            self.config.set('password', 'punctuation_in_password', value)

    def save(self):
        with open(self.config_path, 'w') as file:
            self.config.write(file)
