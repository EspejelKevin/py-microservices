from abc import ABCMeta, abstractmethod

from models import User
from schemas import RegisterUser


class DBService(metaclass=ABCMeta):
    @abstractmethod
    def is_up(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get(self, username: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def save(self, user: RegisterUser) -> bool:
        raise NotImplementedError
