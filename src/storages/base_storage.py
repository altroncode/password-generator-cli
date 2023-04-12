import abc

from src import config, password


class BaseStorage(abc.ABC):

    def __init__(self, settings: config.data_models.BaseModel) -> None:
        self._settings = settings

    @abc.abstractmethod
    def keep(self, password_: password.Password, credentials_: str, note: str) -> None:
        pass
