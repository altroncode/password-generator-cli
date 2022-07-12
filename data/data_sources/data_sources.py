from __future__ import annotations
import configparser
import argparse
import pathlib
import types
import typing
import abc


def cast_value_to_type(value: str, value_type: type):
    if value_type == bool:
        match value:
            case 'True' | 'true' | 'Yes' | 'yes' | '1':
                return True
            case 'False' | 'false' | 'No' | 'no' | '0':
                return False
    return value_type(value)


class BaseDataSource(metaclass=abc.ABCMeta):
    _order: list[BaseDataSource]

    @abc.abstractmethod
    def provide(self, key: tuple[str, ...], value_type: type) -> typing.Any:
        pass

    @abc.abstractmethod
    def __add__(self, other: 'BaseDataSource'):
        pass


class WritableDataSource(BaseDataSource, metaclass=abc.ABCMeta):

    def set(self, *args, **kwargs) -> None:
        pass


class IniDataSource(WritableDataSource):
    __slots__ = ('_parser', '_separator', '_parser_path', '_parser', '_order')

    def __init__(self, path: str | pathlib.Path, separator=', ') -> None:
        self._parser = configparser.ConfigParser()
        self._separator = separator
        self._parser_path = path
        self._parser.read(self._parser_path)
        self._order: list[BaseDataSource] = [self]

    def provide(self, key: tuple[str, ...], value_type: type) -> typing.Any:
        if isinstance(value_type, types.GenericAlias):
            primary_type, secondary_type = value_type.__origin__, value_type.__args__[0]
            if primary_type in (list, tuple):
                values = self._parser.get(key[0], key[1], fallback=[]).split(self._separator)
                for index, value in enumerate(values):
                    values[index] = cast_value_to_type(value, secondary_type)
                return primary_type(values)
        else:
            value = self._parser.get(key[0], key[1], fallback=None)
            return cast_value_to_type(value, value_type) if value is not None else None

    def set(self, key: tuple[str, ...], value: str) -> None:
        self._parser.set(key[0], key[1], value)
        with open(self._parser_path, 'w') as file:
            self._parser.write(file)

    def __add__(self, other: BaseDataSource) -> BaseDataSource:
        self._order.append(other)
        return OtherDataSource(self._order)


class CLIArgumentsDataSource(BaseDataSource):
    __slots__ = ('_order', 'arguments')

    def __init__(self, arguments: argparse.Namespace):
        self._order: list[BaseDataSource] = [self]
        self.arguments = arguments

    def provide(self, key: tuple[str, ...], value_type: type = str) -> typing.Any:
        if hasattr(self.arguments, key[-1]):
            return getattr(self.arguments, key[-1])
        return None

    def __add__(self, other: BaseDataSource) -> BaseDataSource:
        self._order.append(other)
        return OtherDataSource(self._order)


class OtherDataSource(WritableDataSource):
    __slots__ = ('_order',)

    def __init__(self, order: list[BaseDataSource]) -> None:
        self._order = order

    def provide(self, key: tuple[str, ...], value_type: type = str) -> typing.Any:
        for data_source in self._order:
            value = data_source.provide(key, value_type)
            if value is not None:
                return value

    def set(self, key: tuple[str, ...], value: typing.Any) -> None:
        for data_source in self._order:
            if isinstance(data_source, WritableDataSource):
                data_source.set(key, value)
                break

    def __add__(self, other: BaseDataSource) -> BaseDataSource:
        self._order.append(other)
        return OtherDataSource(self._order)
