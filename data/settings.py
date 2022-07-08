"""Module for setting project"""
import typing

from data import base_data_model
from data._field import Field


SETTINGS_PATH = 'data/settings.ini'
DATA_PATH = 'data/app_data.ini'


class GeneralSettings(base_data_model.BaseDataModel):
    _section_name = 'general'

    storage = Field(value_type=list)


class PasswordSettings(base_data_model.BaseDataModel):
    _section_name: str = 'password'

    default_length = Field(value_type=int)
    digits_in_password = Field(value_type=bool)
    capital_letters_in_password = Field(value_type=bool)
    small_letters_in_password = Field(value_type=bool)
    punctuation_in_password = Field(value_type=bool)
