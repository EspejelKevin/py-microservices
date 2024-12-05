import os
from contextlib import contextmanager
from typing import Optional

from controllers import (HealthChekController, LoginController,
                         RegisterController)
from database import Database
from dependency_injector import containers, providers
from repositories import UserRepository
from services import UserService


class DatabasesContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    mysql = providers.Singleton(Database, url=config.databases.mysql.url)


class RepositoriesContainer(containers.DeclarativeContainer):
    databases: DatabasesContainer = providers.DependenciesContainer()
    user_repository = providers.Singleton(
        UserRepository, session_factory=databases.mysql.provided.session)


class ServicesContainer(containers.DeclarativeContainer):
    repositories: RepositoriesContainer = providers.DependenciesContainer()
    user_service = providers.Factory(
        UserService, user_repository=repositories.user_repository)


class ControllersContainer(containers.DeclarativeContainer):
    services: ServicesContainer = providers.DependenciesContainer()
    health_check = providers.Factory(
        HealthChekController, user_service=services.user_service)
    register_user = providers.Factory(
        RegisterController, user_service=services.user_service
    )
    login_user = providers.Factory(
        LoginController, user_service=services.user_service
    )


class BaseContainer(containers.DeclarativeContainer):
    config_path = f'{os.path.dirname(__file__)}/config.json'
    config = providers.Configuration(json_files=[config_path])
    databases = providers.Container(DatabasesContainer, config=config)
    repositories = providers.Container(
        RepositoriesContainer, databases=databases)
    services = providers.Container(
        ServicesContainer, repositories=repositories)
    controllers = providers.Container(ControllersContainer, services=services)


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
