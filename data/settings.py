"""Module for setting project"""
import typing

from data._field import Field
from data.data_sources import data_sources

SETTINGS_PATH = 'data/settings.ini'
DATA_PATH = 'data/app_data.ini'


class PasswordSettings:
    __section_name: str = 'password'
    default_length = Field(value_type=int)
    digits_in_password = Field(value_type=bool)
    capital_letters_in_password = Field(value_type=bool)
    small_letters_in_password = Field(value_type=bool)
    punctuation_in_password = Field(value_type=bool)

    def __init__(self, source: data_sources.BaseDataSource) -> None:
        self.__source = source
        for field_name, field in self:
            key = (self.__section_name, field_name)
            value = self.__source.provide(key, field.value_type)
            field.set_key(key)
            field.set_data_source(self.__source)
            field.set_value(value)

    def __getitem__(self, item: str) -> Field | None:
        field = self.__class__.__dict__[item]
        return field if isinstance(field, Field) else None

    def __setitem__(self, key: str, value: typing.Any) -> None:
        field = self[key]
        if field is not None:
            field.value = value

    def __iter__(self) -> typing.Generator[str, Field]:
        for field_name, field in self.__class__.__dict__.items():
            if isinstance(field, Field):
                yield field_name, field

    def save(self) -> None:
        for _, field in self:
            field.save()
