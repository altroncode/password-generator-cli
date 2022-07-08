import abc


class BaseStorage(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def keep(self, password, password_info: str) -> None:
        pass
