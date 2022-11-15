import typing

import utils
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


class CredentialSentToTelegramBuilder:

    def __init__(self):
        self._credentials = ''

    def get_password_info(self) -> str:
        return self._credentials

    def set_platform(self, platform: str) -> str:
        self._credentials += f'\n*Platform*: {utils.escape_message(platform)}'
        self._credentials.lstrip('\n')
        return self._credentials

    def set_login(self, login: str) -> str:
        self._credentials += f'\n*Login*: {utils.escape_message(login)}'
        self._credentials.lstrip('\n')
        return self._credentials

    def set_email(self, email: str) -> str:
        self._credentials += f'\n*Email*: {utils.escape_message(email)}'
        self._credentials.lstrip('\n')
        return self._credentials


class CredentialsDirector:
    def __init__(self, credentials_settings: settings.CredentialsSettings):
        self._settings = credentials_settings

    def create_password_info(self, builder: BaseCredentialsBuilder):
        platform = self._settings.platform
        login = self._settings.login
        if platform is not None:
            builder.set_platform(platform)
        if login is not None:
            builder.set_login(login)
        for email in self._settings.emails:
            builder.set_email(email)

        return builder.get_credentials()
