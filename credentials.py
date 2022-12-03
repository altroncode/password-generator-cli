import typing

import text_processing
from config import settings


class BaseCredentialsBuilder(typing.Protocol):

    def get_credentials(self) -> str:
        pass

    def set_platform(self, platform: str) -> str:
        pass

    def set_login(self, login: str) -> str:
        pass

    def set_email(self, email: str) -> str:
        pass


class CredentialsSentToTelegramBuilder:

    def __init__(self):
        self._credentials = ''
        self.__text_processing = text_processing.TelegramTextProcessing()

    def get_password_info(self) -> str:
        return self._credentials

    def set_platform(self, platform: str) -> str:
        self._credentials += f'\n*Platform*: {self.__text_processing.escape_text(platform)}'
        self._credentials.lstrip('\n')
        return self._credentials

    def set_login(self, login: str) -> str:
        self._credentials += f'\n*Login*: {self.__text_processing.escape_text(login)}'
        self._credentials.lstrip('\n')
        return self._credentials

    def set_email(self, email: str) -> str:
        self._credentials += f'\n*Email*: {self.__text_processing.escape_text(email)}'
        self._credentials.lstrip('\n')
        return self._credentials


class CredentialsDirector:
    def __init__(self, credentials_settings: settings.CredentialsSettings):
        self._settings = credentials_settings

    def create_credentials(self, builder: BaseCredentialsBuilder):
        platform = self._settings.platform
        login = self._settings.login
        if platform is not None:
            builder.set_platform(platform)
        if login is not None:
            builder.set_login(login)
        for email in self._settings.emails:
            builder.set_email(email)

        return builder.get_credentials()
