"""Module for managing dynamic app data"""
import typing

from data._field import Field
from data.data_sources import data_sources


class PasswordInfoData:
    """Data for whole project"""

    _section_name: str = 'password_info'

    platform = Field(value_type=str)
    username = Field(value_type=str)
    emails = Field(value_type=list)
    note = Field(value_type=str)

    def __init__(self, source: data_sources.BaseDataSource) -> None:
        self.__source = source
        for field_name, field in self:
            key = (self._section_name, field_name)
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

    def __iter__(self) -> typing.Generator[tuple[str, Field], None, None]:
        for field_name, field in self.__class__.__dict__.items():
            if isinstance(field, Field):
                yield field_name, field

    def save(self) -> None:
        for _, field in self:
            field.save()


class TelegramData:
    """Data for work with telegram"""

    _section_name: str = 'telegram'
    user_id = Field(value_type=int)
    token = Field(value_type=str)
    last_message_id = Field(value_type=int)

    def __init__(self, source: data_sources.BaseDataSource) -> None:
        self.__source = source
        for field_name, field in self:
            key = (self._section_name, field_name)
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

    def __iter__(self) -> typing.Generator[tuple[str, Field], None, None]:
        for field_name, field in self.__class__.__dict__.items():
            if isinstance(field, Field):
                yield field_name, field

    def save(self) -> None:
        for _, field in self:
            field.save()
