from .db_service import DBService


class AuthService(DBService):
    def __init__(self, auth_repository: DBService) -> None:
        self.auth_repository = auth_repository

    def is_up(self) -> dict:
        return self.auth_repository.is_up()

    def get(self, user_id: str) -> str:
        return self.auth_repository.get(user_id)

    def set(self, user_id: str, token: str, ex: int) -> bool:
        return self.auth_repository.set(user_id, token, ex)
