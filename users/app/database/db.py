from contextlib import contextmanager, suppress
from typing import Iterator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session


class DBSession:
    def __init__(self, url: str, **connect_args: dict) -> None:
        self._engine = create_engine(url=url, connect_args=connect_args)
        self._session = Session(
            self._engine, autocommit=False, autoflush=False)

    def __enter__(self):
        return self

    def get_client(self) -> Session:
        return self._session

    def is_up(self) -> dict:
        data = {
            'success': True,
            'dependency': 'MySQL DB',
            'error': None
        }

        try:
            self._session.execute(text('SELECT 1'))
        except Exception as e:
            data['success'] = False
            data['error'] = str(e)

        return data

    def __exit__(self, *exc) -> None:
        self._session.close()


class Database:
    def __init__(self, url: str, **connect_args: dict) -> None:
        self.__session = DBSession(url, **connect_args)

    @contextmanager
    def session(self) -> Iterator[DBSession]:
        with self.__session as session:
            yield session
