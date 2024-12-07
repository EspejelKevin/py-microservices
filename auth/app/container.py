from contextlib import contextmanager
from typing import Optional

from config import Config
from controllers import (HealthChekController, TokenController,
                         VerifyTokenController)
from database import Database
from dependency_injector import containers, providers
from repositories import AuthRepository
from services import AuthService


class DatabasesContainer(containers.DeclarativeContainer):
    config = providers.Dependency(Config)
    redis = providers.Singleton(
        Database, url=config.provided.redis_url)


class RepositoriesContainer(containers.DeclarativeContainer):
    databases: DatabasesContainer = providers.DependenciesContainer()
    auth_repository = providers.Singleton(
        AuthRepository, session_factory=databases.redis.provided.session)


class ServicesContainer(containers.DeclarativeContainer):
    repositories: RepositoriesContainer = providers.DependenciesContainer()
    auth_service = providers.Factory(
        AuthService, auth_repository=repositories.auth_repository)


class ControllersContainer(containers.DeclarativeContainer):
    config = providers.Dependency(Config)
    services: ServicesContainer = providers.DependenciesContainer()
    health_check = providers.Factory(
        HealthChekController, auth_service=services.auth_service)
    token = providers.Factory(
        TokenController, auth_service=services.auth_service, config=config)
    verify_token = providers.Factory(
        VerifyTokenController, auth_service=services.auth_service, config=config
    )


class BaseContainer(containers.DeclarativeContainer):
    config = providers.Singleton(Config)
    databases = providers.Container(DatabasesContainer, config=config)
    repositories = providers.Container(
        RepositoriesContainer, databases=databases)
    services = providers.Container(
        ServicesContainer, repositories=repositories)
    controllers = providers.Container(
        ControllersContainer, services=services, config=config)


class AppContainer:
    container: Optional[BaseContainer] = None

    @classmethod
    @contextmanager
    def scope(cls):
        try:
            cls.container.services.init_resources()
            yield cls.container
        finally:
            cls.container.services.shutdown_resources()

    @classmethod
    def init(cls) -> None:
        if cls.container is None:
            cls.container = BaseContainer()
