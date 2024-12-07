from pydantic_settings import BaseSettings


class Config(BaseSettings):
    mysql_url: str
    port: int
    token_service_url: str
