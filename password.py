import secrets
import string

import data


class Password:
    def __init__(self, settings: data.settings.PasswordSettings):
        self._settings = settings
        self._password = self.create_password()

    def _get_symbols(self) -> str:
        symbols = ''
        if self._settings.digits_in_password:
            symbols += string.digits
        if self._settings.capital_letters_in_password:
            symbols += string.ascii_uppercase
        if self._settings.small_letters_in_password:
            symbols += string.ascii_lowercase
        if self._settings.punctuation_in_password:
            symbols += string.punctuation
        return symbols

    def create_password(self) -> str:
        symbols = self._get_symbols()
        return "".join(secrets.choice(symbols) for _ in range(self._settings.default_length))

    def __str__(self):
        return self._password

    def __len__(self):
        return len(self._password)
