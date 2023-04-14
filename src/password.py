import random
import secrets
import string

import config


class PasswordFactory:

    def __init__(self, settings: config.settings.PasswordSettings):
        self._settings = settings

    def create_password(self) -> 'Password':
        length = self._settings.length
        next_symbol: int = 0
        password_symbols: list[str] = [''] * length
        symbol_groups = self._get_symbol_groups()
        for i, symbols in enumerate(symbol_groups):
            password_symbols[next_symbol:] = [
                secrets.choice(symbols) for _ in range(length - next_symbol)
            ]
            next_symbol = random.randint(next_symbol + 1, length - (len(symbol_groups) - i))
        random.shuffle(password_symbols)
        return Password(''.join(password_symbols))

    def _get_symbol_groups(self):
        symbol_groups: dict = {
            string.digits: self._settings.is_digits,
            string.ascii_uppercase: self._settings.is_capital_letters,
            string.ascii_lowercase: self._settings.is_small_letters,
            string.punctuation: self._settings.is_punctuation
        }
        return [key for key, value in symbol_groups.items() if value]


class Password:
    __slots__ = ('_settings', '_password')

    def __init__(self, password: str):
        self._password = password

    def __str__(self):
        return self._password

    def __repr__(self):
        return f'{type(self)}(settings={self._settings})'

    def __len__(self):
        return len(self._password)
