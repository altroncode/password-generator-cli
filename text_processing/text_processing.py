import abc
import typing


__all__ = ('BaseTextProcessing', 'SimpleTextProcessing', 'TelegramFormatting')


TelegramFormatting: typing.TypeAlias = typing.Literal['bold', 'code', 'pre', 'underline', 'strike']


class BaseTextProcessing(abc.ABC):
    def escape_text(self, text: str) -> str:
        pass

    def format_text(self, text: str, formatting: str) -> str:
        pass

    def color_text(self, text: str, color: str) -> str:
        pass


class SimpleTextProcessing(BaseTextProcessing):
    def escape_text(self, text: str) -> str:
        return ''.join(f'\\{symbol}' for symbol in text)

    def color_text(self, text: str, color: str) -> str:
        return f'{color}{text}\x1b[0m'

    def format_text(self, text: str, formatting: str) -> str:
        return text


class TelegramTextProcessing(BaseTextProcessing):

    def __init__(self):
        self.__simple_text_processing = SimpleTextProcessing()

    def escape_text(self, text: str) -> str:
        return self.__simple_text_processing.escape_text(text)

    def color_text(self, text: str, color: str) -> str:
        return text

    def format_text(self, text: str, formatting: TelegramFormatting) -> str:
        pattern = self.__get_formatting_pattern(formatting)
        return pattern.format(text)

    def __get_formatting_pattern(self, formatting: TelegramFormatting) -> str:
        tags = self.__get_formatting_tags()
        tag = tags[formatting]
        return f'<{tag}>{{}}<\\{tag}>'

    @staticmethod
    def __get_formatting_tags() -> dict[TelegramFormatting: str]:
        return {
            'bold': 'b', 'italic': 'i',
            'underline': 'u', 'strike': 's',
            'code': 'code', 'pre': 'pre'
        }
