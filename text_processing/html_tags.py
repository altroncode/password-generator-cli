import abc
import typing


class HTMLTag(abc.ABC):
    name: str
    attributes: dict[str, typing.Any]

    @abc.abstractmethod
    def __init__(self, **attributes) -> None:
        pass


class TelegramTag(HTMLTag, abc.ABC):
    pass


class BoldTag(TelegramTag):
    def __init__(self) -> None:
        self.name = 'b'
        self.attributes = {}


class ItalicTag(TelegramTag):
    def __init__(self) -> None:
        self.name = 'i'
        self.attributes = {}


class UnderlineTag(TelegramTag):
    def __init__(self) -> None:
        self.name = 'u'
        self.attributes = {}


class StrikeTag(TelegramTag):
    def __init__(self) -> None:
        self.name = 's'
        self.attributes = {}


class SpoilerTag(TelegramTag):
    def __init__(self) -> None:
        self.name = 'tg-spoiler'
        self.attributes = {}


class LinkTag(TelegramTag):
    def __init__(self, href: str) -> None:
        self.name = 'a'
        self.attributes = {'href': href}


class CodeTag(TelegramTag):
    def __init__(self, language: str) -> None:
        self.name = 'code'
        self.attributes = {'class': f'language-{language}'}


class PreTag(TelegramTag):
    def __init__(self) -> None:
        self.name = 'pre'
        self.attributes = {}
