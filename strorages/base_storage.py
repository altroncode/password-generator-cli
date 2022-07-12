import abc


class BaseStorage(abc.ABC):

    @abc.abstractmethod
    def keep(self, password, password_info: str) -> None:
        pass
