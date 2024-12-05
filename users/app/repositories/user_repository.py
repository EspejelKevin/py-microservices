from models import User
from schemas import RegisterUser
from services import DBService
from sqlalchemy import select
from sqlalchemy.orm import Session


class UserRepository(DBService):
    def __init__(self, session_factory) -> None:
        self.session_factory = session_factory

    def is_up(self) -> dict:
        with self.session_factory() as session:
            data: dict = session.is_up()
            return data

    def get(self, username: str) -> User:
        with self.session_factory() as session:
            client: Session = session.get_client()
            return client.query(User).filter(User.username == username).first()

    def save(self, user: RegisterUser) -> bool:
        with self.session_factory() as session:
            client: Session = session.get_client()
            client.add(User(**user.model_dump()))
            client.commit()
            return True
