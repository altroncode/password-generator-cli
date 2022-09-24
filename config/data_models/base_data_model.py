import typing

from config.data_sources import data_sources
from config.data_models.field import Field


class BaseModel:
    _section_name: str

    def __init__(self, source: data_sources.BaseDataSource) -> None:
        self.__source = source
        for field_name, field in self:
            if field.init:
                key = (self._section_name, field.alias or field_name)
                value = self.__source.provide(key, self.__annotations__[field_name])
                field.set_key(key)
                field.set_data_source(self.__source)
                if value is not None:
                    field.set_value(value)

    def __getitem__(self, item: str):
        return self.__class__.__dict__.get(item) or self.__dict__.get(item)

    def __setitem__(self, key: str, value: typing.Any) -> None:
        self.__dict__[key] = value

    def __iter__(self) -> typing.Generator[tuple[str, Field], None, None]:
        for field_name, field in self.__class__.__dict__.items():
            if isinstance(field, Field):
                yield field_name, field

    def save(self) -> None:
        for _, field in self:
            field.save()
