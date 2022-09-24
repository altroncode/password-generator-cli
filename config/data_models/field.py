import typing

from config.data_sources import data_sources


class Field:
    __slots__ = ('data_source', 'frozen', 'init', 'key', 'value', 'alias')

    def __init__(self, key: tuple[str] = None, *, frozen: bool = False, init: bool = True,
                 default=None, alias: str | None = None):
        self.data_source: data_sources.BaseDataSource | None = None
        self.key = key
        self.frozen = frozen
        self.init = init
        self.alias = alias
        self.value = default

    def set_key(self, key: tuple[str, ...]) -> None:
        self.key = key

    def set_value(self, value: typing.Any) -> None:
        self.value = value

    def set_data_source(self, data_source: data_sources.BaseDataSource) -> None:
        self.data_source = data_source

    def __get__(self, instance: object, owner: type) -> typing.Any:
        return self.value

    def __set__(self, key, value) -> None:
        self.set_value(value)

    def save(self) -> None:
        if isinstance(self.data_source, data_sources.WritableDataSource) and not self.frozen:
            self.data_source.set(self.key, self.value)
