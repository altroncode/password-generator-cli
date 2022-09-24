import typing

import utils
from config import settings


class BasePasswordInfoBuilder(typing.Protocol):

    def get_password_info(self) -> str:
        pass

    def set_platform(self, platform: str) -> str:
        pass

    def set_login(self, login: str) -> str:
        pass

    def set_email(self, email: str) -> str:
        pass

    def set_note(self, note: str) -> str:
        pass


class TelegramPasswordInfoBuilder:

    def __init__(self):
        self._password_info = ''

    def get_password_info(self) -> str:
        return self._password_info

    def set_platform(self, platform: str) -> str:
        self._password_info += f'\n*Platform*: {utils.escape_message(platform)}'
        self._password_info.lstrip('\n')
        return self._password_info

    def set_login(self, login: str) -> str:
        self._password_info += f'\n*Login*: {utils.escape_message(login)}'
        self._password_info.lstrip('\n')
        return self._password_info

    def set_email(self, email: str) -> str:
        self._password_info += f'\n*Emails*: {utils.escape_message(email)}'
        self._password_info.lstrip('\n')
        return self._password_info

    def set_note(self, note: str) -> str:
        self._password_info += f'\n*Note*: {utils.escape_message(note)}'
        self._password_info.lstrip('\n')
        return self._password_info


class PasswordInfoDirector:
    def __init__(self, password_info_settings: settings.PasswordInfoSettings):
        self._settings = password_info_settings

    def create_password_info(self, builder: BasePasswordInfoBuilder):
        platform = self._settings.platform
        login = self._settings.login
        note = self._settings.note
        if platform is not None:
            builder.set_platform(platform)
        if login is not None:
            builder.set_login(login)
        for email in self._settings.emails:
            builder.set_email(email)
        if note is not None:
            builder.set_note(note)

        return builder.get_password_info()
