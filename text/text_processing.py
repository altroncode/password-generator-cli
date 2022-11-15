import typing


class BaseTextProcessing(typing.Protocol):
    def escape_text(self):
        pass

    def format_text(self):
        pass

    def color_text(self):
        pass


class SimpleTextProcessing:

    @staticmethod
    def escape_text(text: str) -> str:
        return ''.join(f'\\{symbol}' for symbol in text)
