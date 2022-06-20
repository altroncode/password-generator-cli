import secrets
import string


class Password:
    def __init__(self, length: int, is_digit: bool, is_letter: bool, is_punctuation: bool):
        self.length = length
        self.is_digit = is_digit
        self.is_letter = is_letter
        self.is_punctuation = is_punctuation
        self._password = self.create_password()

    def _get_symbols(self) -> str:
        symbols = ''
        if self.is_digit:
            symbols += string.digits
        if self.is_letter:
            symbols += string.ascii_letters
        if self.is_punctuation:
            symbols += string.punctuation
        return symbols

    def create_password(self) -> str:
        symbols = self._get_symbols()
        return str().join(secrets.choice(symbols) for _ in range(self.length))

    def __str__(self):
        return self._password

    def __len__(self):
        return len(self._password)


