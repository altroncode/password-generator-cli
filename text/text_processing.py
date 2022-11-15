import abc


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
