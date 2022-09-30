import abc
import argparse
import configparser
import dataclasses
import pathlib
import types
import typing


@dataclasses.dataclass
class Key:
    sections: tuple[str]
    key: str
    env: str


def cast_value_to_type(value: str, value_type: type):
    if value_type == str:
        return value
    if value_type == bool:
        match value:
            case 'True' | 'true' | 'Yes' | 'yes' | '1':
                return True
            case 'False' | 'false' | 'No' | 'no' | '0' | '':
                return False
    if value_type in (int, float):
        if not value.replace('.', '').isdigit():
            return None
    return value_type(value) if value else None


class BaseDataSource(abc.ABC):

    @abc.abstractmethod
    def provide(self, key: Key, value_type: type) -> typing.Any:
        pass

    @abc.abstractmethod
    def check_is_key_exists(self, key: Key) -> bool:
        pass

    @abc.abstractmethod
    def __add__(self, other: 'BaseDataSource'):
        pass


class WritableDataSource(BaseDataSource, abc.ABC):

    @abc.abstractmethod
    def set(self, *args, **kwargs) -> None:
        pass


class OtherDataSource(WritableDataSource):
    __slots__ = ('_order',)

    def __init__(self, order: list[BaseDataSource]) -> None:
        self._order = order

    def provide(self, key: Key, value_type: type) -> typing.Any:
        for data_source in self._order:
            value = data_source.provide(key, value_type)
            if value is not None:
                return value

    def check_is_key_exists(self, key: Key) -> bool:
        for data_source in self._order:
            if data_source.check_is_key_exists(key):
                return True
        return False

    def set(self, key: Key, value: typing.Any, env: str = None) -> None:
        for data_source in self._order:
            if isinstance(data_source, WritableDataSource):
                if data_source.check_is_key_exists(key):
                    data_source.set(key, value)
                    break

    def __add__(self, other: BaseDataSource) -> 'OtherDataSource':
        return OtherDataSource(self._order + [other])


class EnvDataSource(WritableDataSource):
    def __init__(self, path: str | pathlib.Path):
        self.__path = path

    def provide(self, key: Key, value_type: type = str) -> typing.Any:
        if not self.check_is_key_exists(key):
            return None
        lines = open(self.__path, 'r').readlines()
        for i, line in enumerate(lines):
            value = line.split('=')[1].replace('\n', '').strip()
            if line.split('=')[0] == key.env:
                if isinstance(value_type, types.GenericAlias):
                    secondary_type = value_type.__args__[0]
                    value = value.replace('[', '').replace(']', '')
                    value = value.replace("'", '').replace('"', '')
                    return [secondary_type(j) for j in value.split(', ')]
                return cast_value_to_type(value, value_type) if value != '' else None

    def check_is_key_exists(self, key: Key) -> bool:
        for line in open(self.__path, 'r').readlines():
            if line.split('=')[0] == key.env:
                return True

    def set(self, key: Key, value: typing.Any) -> None:
        lines = open(self.__path, 'r').readlines()
        for i, line in enumerate(lines):
            if not line.endswith('\n'):
                lines[i] = f'{line}\n'
            if line.split('=')[0] == key.env:
                lines[i] = f'{key.env}={value}\n'
                break
        else:
            lines.append(f'{key.env}={value}\n')
        file = open(self.__path, 'w')
        file.writelines(lines)

    def __add__(self, other: 'BaseDataSource') -> OtherDataSource:
        return OtherDataSource([self, other])


class IniDataSource(WritableDataSource):
    __slots__ = ('_parser', '_separator', '_parser_path', '_parser')

    def __init__(self, path: str | pathlib.Path, separator=', ') -> None:
        self._parser = configparser.ConfigParser()
        self._separator = separator
        self._parser_path = path
        self._parser.read(self._parser_path)

    def provide(self, key: Key, value_type: type) -> typing.Any:
        if not self.check_is_key_exists(key):
            return None
        if isinstance(value_type, types.GenericAlias):
            primary_type, secondary_type = value_type.__origin__, value_type.__args__[0]
            if primary_type in (list, tuple):
                values = self._parser.get(key.sections[-1], key.key, fallback='')
                values = values.split(self._separator)
                for index, value in enumerate(values):
                    values[index] = cast_value_to_type(value, secondary_type)
                return primary_type(values)
        else:
            value = self._parser.get(key.sections[-1], key.key, fallback=None)
            return cast_value_to_type(value, value_type) if value is not None and value != '' else None

    def check_is_key_exists(self, key: Key) -> bool:
        return self._parser.get(key.sections[-1], key.key, fallback=None) is not None

    def set(self, key: Key, value: str) -> None:
        self._parser.set(key.sections[0], key.key, value)
        with open(self._parser_path, 'w') as file:
            self._parser.write(file)

    def __add__(self, other: BaseDataSource) -> BaseDataSource:
        return OtherDataSource([self, other])


class CLIArgumentsDataSource(BaseDataSource):
    __slots__ = ('arguments',)

    def __init__(self, arguments: argparse.Namespace):
        self.arguments = arguments

    def provide(self, key: Key, value_type: type = str) -> typing.Any:
        if self.check_is_key_exists(key):
            return getattr(self.arguments, key.key)
        return None

    def check_is_key_exists(self, key: Key) -> bool:
        return hasattr(self.arguments, key.key)

    def __add__(self, other: BaseDataSource) -> BaseDataSource:
        return OtherDataSource([self, other])
