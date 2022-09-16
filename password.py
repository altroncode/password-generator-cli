import random
import secrets
import string

import data


class Password:
    __slots__ = ('_settings', '_password')

    def __init__(self, settings: data.settings.PasswordSettings):
        self._settings = settings
        self._password = self.create_password()

    def create_password(self) -> str:
        length: int = self._settings.length
        next_symbol: int = 0
        password_symbols: list[str] = [''] * length
        symbol_groups = self._get_symbol_groups()
        for i, symbols in enumerate(symbol_groups):
            password_symbols[next_symbol:] = [
                secrets.choice(symbols) for _ in range(length - next_symbol)
            ]
            next_symbol = random.randint(i+1, length-(len(symbol_groups) - i))
        random.shuffle(password_symbols)
        return ''.join(password_symbols)

    def _get_symbol_groups(self):
        symbols: dict = {
            string.digits: self._settings.is_digits,
            string.ascii_uppercase: self._settings.is_capital_letters,
            string.ascii_lowercase: self._settings.is_small_letters,
            string.punctuation: self._settings.is_punctuation
        }
        return {key: value for key, value in symbols.items() if value}

    def __str__(self):
        return self._password

    def __repr__(self):
        return f'{type(self)}(settings={self._settings})'

    def __len__(self):
        return len(self._password)
