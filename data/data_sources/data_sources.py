import configparser
import argparse
import pathlib
import typing
import abc


class BaseDataSource(metaclass=abc.ABCMeta):
    _order: list['BaseDataSource']

    @abc.abstractmethod
    def provide(self, key: tuple[str, ...], value_type: type = str) -> typing.Any:
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

    def provide(self, key: tuple[str, ...], value_type: type = str) -> typing.Any:
        value = self._parser.get(key[0], key[1])
        if value is not None:
            if value_type == str:
                return value
            if value_type == bool:
                if value == 'True':
                    return True
                elif value == 'False':
                    return False
            if isinstance(value, typing.Iterable):
                value = value.split(self._separator)
            return value_type(value)
        return None

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
