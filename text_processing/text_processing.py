import abc

from text_processing import html_tags


__all__ = ('BaseTextProcessing', 'SimpleTextProcessing', 'HTMLProcessing', 'TelegramTextProcessing')


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


class HTMLProcessing(BaseTextProcessing):

    def escape_text(self, text: str) -> str:
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

    def color_text(self, text: str, color: str) -> str:
        return text

    def format_text(self, text: str, tag: html_tags.HTMLTag) -> str:
        html_attributes = ' '.join([f'{name}="{value}"' for name, value in tag.attributes.items()])
        pattern = f'<{tag.name} {html_attributes}>{{}}<\\{tag.name}>'
        return pattern.format(text)


class TelegramTextProcessing(BaseTextProcessing):

    def __init__(self):
        self.__html_processing = HTMLProcessing()

    def escape_text(self, text: str) -> str:
        return self.__html_processing.escape_text(text)

    def color_text(self, text: str, color: str) -> str:
        return text

    def format_text(self, text: str, formatting_tag: html_tags.TelegramTag):
        return self.__html_processing.format_text(text, formatting_tag)
