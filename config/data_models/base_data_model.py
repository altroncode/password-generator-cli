import typing

from config.data_models.field import Field
from config.data_sources import data_sources


class BaseModel:
    _sections: tuple[str] = ()

    def __init__(self, source: data_sources.BaseDataSource) -> None:
        self.__source = source
        for field_name, field in self:
            if not field.init:
                continue
            key = data_sources.Key(self._sections, field_name, field.env)
            field.set_data_source(self.__source).set_key(key).set_value_type(
                self.__annotations__[field_name]).set_value(
                field.get_value_from_data_source()
            )

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
