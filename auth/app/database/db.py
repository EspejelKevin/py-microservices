from contextlib import contextmanager
from typing import Iterator

import redis


class DBSession:
    def __init__(self, url: str, **connect_args: dict) -> None:
        self._client: redis.Redis = redis.from_url(url, **connect_args)

    def __enter__(self):
        return self

    def get_client(self) -> redis.Redis:
        return self._client

    def is_up(self) -> dict:
        data = {
            'success': True,
            'dependency': 'Redis DB',
            'error': None
        }

        try:
            self._client.ping()
        except Exception as e:
            data['success'] = False
            data['error'] = str(e)

        return data

    def __exit__(self, *exc) -> None:
        self._client.close()


class Database:
    def __init__(self, url: str, **connect_args: dict) -> None:
        self.__session = DBSession(url, **connect_args)

    @contextmanager
    def session(self) -> Iterator[DBSession]:
        with self.__session as session:
            yield session
