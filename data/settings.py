"""Module for setting project"""
from data import base_data_model
from data._field import Field


SETTINGS_PATH = 'password-generator/data/settings.ini'
DATA_PATH = 'password-generator/data/app_data.ini'


class GeneralSettings(base_data_model.BaseDataModel):
    _section_name = 'general'

    storages: list[str] = Field()


class PasswordSettings(base_data_model.BaseDataModel):
    _section_name: str = 'password'

    default_length: int = Field()
    digits_in_password: bool = Field()
    capital_letters_in_password: bool = Field()
    small_letters_in_password: bool = Field()
    punctuation_in_password: bool = Field()
