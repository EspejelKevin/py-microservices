from abc import ABCMeta, abstractmethod


class DBService(metaclass=ABCMeta):
    @abstractmethod
    def is_up(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get(self, user_id: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def set(self, user_id: str, token: str, ex: int) -> bool:
        raise NotImplementedError
