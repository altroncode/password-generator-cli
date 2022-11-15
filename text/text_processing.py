class SimpleTextProcessing:

    @staticmethod
    def escape_text(text: str) -> str:
        return ''.join(f'\\{symbol}' for symbol in text)
