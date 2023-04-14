import abc
import dataclasses
import typing

import config.data_models
import credentials
import password
import storages
from config import settings
from config.data_sources import data_sources


@dataclasses.dataclass
class PasswordSavingStrategy:
    __storage: typing.Type[storages.BaseStorage | storages.BaseStorageWithArchive]
    __storage_settings: typing.Type[config.data_models.BaseModel]
    __credentials_settings: settings.CredentialsSettings
    __credentials_builder: typing.Type[credentials.BaseCredentialsBuilder]
    __data_source: data_sources.BaseDataSource
    __password: password.Password
    __note: str
    __is_archive: bool = None

    def save_password(self) -> None:
        if issubclass(self.__storage, storages.BaseStorageWithArchive):
            storage = self.__storage(self.__storage_settings(self.__data_source), self.__is_archive)
        else:
            storage = self.__storage(self.__storage_settings(self.__data_source))
        credentials_director = credentials.CredentialsDirector(self.__credentials_settings)
        credentials_ = credentials_director.create_credentials(self.__credentials_builder())
        storage.keep(self.__password, credentials_, self.__note)


class BasePasswordSavingStrategy(abc.ABC):
    @abc.abstractmethod
    def save_password(
            self, data_source: data_sources.BaseDataSource,
            credential_settings: settings.CredentialsSettings,
            password_: password.Password, note: str) -> None:
        ...


class PasswordSavingStrategyWithArchive(abc.ABC):
    @abc.abstractmethod
    def save_password(
            self, data_source: data_sources.BaseDataSource,
            credential_settings: settings.CredentialsSettings,
            password_: password.Password, note: str, is_archive: bool) -> None:
        ...


class PasswordSavingToTelegramStrategy(PasswordSavingStrategyWithArchive):
    def save_password(self, data_source: data_sources.BaseDataSource,
                      credentials_settings: settings.CredentialsSettings,
                      password_: password.Password, note: str, is_archive: bool) -> None:
        PasswordSavingStrategy(
            storages.TelegramStorage, settings.TelegramSettings, credentials_settings,
            credentials.CredentialsSentToTelegramBuilder, data_source, password_, note, is_archive
        ).save_password()
