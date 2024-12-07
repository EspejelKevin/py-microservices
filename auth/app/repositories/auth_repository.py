from redis import Redis
from services import DBService


class AuthRepository(DBService):
    def __init__(self, session_factory) -> None:
        self.session_factory = session_factory

    def is_up(self) -> dict:
        with self.session_factory() as session:
            data: dict = session.is_up()
            return data

    def get(self, user_id: str) -> str:
        with self.session_factory() as session:
            client: Redis = session.get_client()
            return client.get(user_id)

    def set(self, user_id: str, token: str, ex: int) -> bool:
        with self.session_factory() as session:
            client: Redis = session.get_client()
            return client.set(user_id, token, ex*60)
