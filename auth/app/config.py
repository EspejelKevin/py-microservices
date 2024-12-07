from pydantic_settings import BaseSettings


class Config(BaseSettings):
    redis_url: str
    redis_expiration_mins: int
    jwt_key: str
    jwt_algorithm: str
    port: int
