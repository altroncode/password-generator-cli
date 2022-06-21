"""Module for setting project"""

import configparser
import os
import pathlib


class PasswordSettings:

    config = configparser.ConfigParser()
    config_path = pathlib.Path(os.curdir) / 'config.ini'
    config.read(config_path)

    def __init__(self):
        self.default_length = self.config.get('password', 'default_length')
        self.digits_in_password = self.config.get('password', '')
        self.capital_letters_in_password = self.config.get('password', 'capital_letters_in_password')
        self.small_letters_in_password = self.config.get('password', 'small_letters_in_password')
        self.punctuation_in_password = self.config.get('password', 'punctuation_in_password')

    def save(self):
        with open(self.config_path, 'w') as file:
            self.config.write(file)
