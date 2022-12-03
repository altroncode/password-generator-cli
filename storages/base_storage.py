import abc

import config.data_models
import password


class BaseStorage(abc.ABC):
    __settings = config.data_models.BaseModel

    @abc.abstractmethod
    def keep(self, password_: password.Password, password_info: str) -> None:
        pass
