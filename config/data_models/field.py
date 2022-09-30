import types
import typing

from config.data_sources import data_sources


class Field:
    __slots__ = ('data_source', 'value_type', 'frozen', 'init', 'key', 'value', 'alias', 'env')

    def __init__(self, key: data_sources.Key = None, *, frozen: bool = False, init: bool = True,
                 default=None, alias: str | None = None, env: str = None):
        self.data_source: data_sources.BaseDataSource | None = None
        self.value_type = None
        self.key = key
        self.frozen = frozen
        self.init = init
        self.alias = alias
        self.value = default
        self.env = env

    def get_value_from_data_source(self) -> typing.Any:
        return self.data_source.provide(self.key, self.value_type)

    def set_value_type(self, value_type: type | types.GenericAlias) -> 'Field':
        self.value_type = value_type
        return self

    def set_key(self, key: data_sources.Key) -> 'Field':
        self.key = key
        return self

    def set_value(self, value: typing.Any) -> 'Field':
        self.value = value
        return self

    def set_data_source(self, data_source: data_sources.BaseDataSource) -> 'Field':
        self.data_source = data_source
        return self

    def __get__(self, instance: object, owner: type) -> typing.Any:
        return self.value

    def __set__(self, key, value) -> None:
        self.set_value(value)

    def save(self) -> None:
        if isinstance(self.data_source, data_sources.WritableDataSource) and not self.frozen:
            if self.data_source.check_is_key_exists(self.key):
                self.data_source.set(self.key, self.value)
