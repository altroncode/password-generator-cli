import abc

import config
import password


class BaseStorage(abc.ABC):

    def __init__(self, settings: config.data_models.BaseModel) -> None:
        self._settings = settings

    @abc.abstractmethod
    def keep(self, password_: password.Password, credentials_: str, note: str) -> None:
        pass


class BaseStorageWithArchive(BaseStorage, abc.ABC):
    def __init__(self, settings: config.data_models.BaseModel, is_archive: bool) -> None:
        super().__init__(settings)
        self._is_archive = is_archive

    @abc.abstractmethod
    def keep(self, password_: password.Password, credentials_: str, note: str) -> None:
        pass
