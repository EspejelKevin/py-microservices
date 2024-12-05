from models import User
from schemas import RegisterUser

from .db_service import DBService


class UserService(DBService):
    def __init__(self, user_repository: DBService) -> None:
        self.user_repository = user_repository

    def is_up(self) -> dict:
        return self.user_repository.is_up()

    def get(self, username: str) -> User:
        return self.user_repository.get(username)

    def save(self, user: RegisterUser) -> bool:
        return self.user_repository.save(user)
