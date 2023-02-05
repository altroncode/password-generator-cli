import typing

import text_processing
from text_processing import html_tags
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

    def get_credentials(self) -> str:
        return self._credentials

    def set_platform(self, platform: str) -> str:
        field_name = self.__text_processing.format_text("Platform", html_tags.BoldTag())
        self._credentials += f'\n{field_name}: {self.__text_processing.escape_text(platform)}'
        return self._credentials.lstrip('\n')

    def set_login(self, login: str) -> str:
        field_name = self.__text_processing.format_text("Login", html_tags.BoldTag())
        self._credentials += f'\n{field_name}: {self.__text_processing.escape_text(login)}'
        return self._credentials.lstrip('\n')

    def set_email(self, email: str) -> str:
        field_name = self.__text_processing.format_text("Email", html_tags.BoldTag())
        self._credentials += f'\n{field_name}: {self.__text_processing.escape_text(email)}'
        return self._credentials.lstrip('\n')


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
