from contextlib import contextmanager
from typing import Optional

from config import Config
from controllers import (HealthChekController, LoginController,
                         RegisterController)
from database import Database
from dependency_injector import containers, providers
from repositories import UserRepository
from services import UserService


class DatabasesContainer(containers.DeclarativeContainer):
    config = providers.Dependency(Config)
    mysql = providers.Singleton(Database, url=config.provided.mysql_url)


class RepositoriesContainer(containers.DeclarativeContainer):
    databases: DatabasesContainer = providers.DependenciesContainer()
    user_repository = providers.Singleton(
        UserRepository, session_factory=databases.mysql.provided.session)


class ServicesContainer(containers.DeclarativeContainer):
    repositories: RepositoriesContainer = providers.DependenciesContainer()
    user_service = providers.Factory(
        UserService, user_repository=repositories.user_repository)


class ControllersContainer(containers.DeclarativeContainer):
    config = providers.Dependency(Config)
    services: ServicesContainer = providers.DependenciesContainer()
    health_check = providers.Factory(
        HealthChekController, user_service=services.user_service)
    register_user = providers.Factory(
        RegisterController, user_service=services.user_service
    )
    login_user = providers.Factory(
        LoginController, user_service=services.user_service, config=config
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
