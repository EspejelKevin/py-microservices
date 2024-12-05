import container
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from schemas import LoginUser, RegisterUser

prefix = '/api/v1/users'
router = APIRouter(prefix=prefix)


@router.get('/liveness', tags=['Health Check'])
def liveness() -> JSONResponse:
    with container.AppContainer.scope() as app:
        health_check_controller = app.controllers.health_check()
        return health_check_controller.liveness()


@router.get('/readiness', tags=['Health Check'])
def readiness() -> JSONResponse:
    with container.AppContainer.scope() as app:
        health_check_controller = app.controllers.health_check()
        return health_check_controller.readiness()


@router.post('/signup', tags=['Users'])
def signup(user: RegisterUser) -> JSONResponse:
    with container.AppContainer.scope() as app:
        register_user_controller = app.controllers.register_user()
        return register_user_controller.execute(user)


@router.post('/login', tags=['Users'])
def login(user: LoginUser) -> JSONResponse:
    with container.AppContainer.scope() as app:
        login_user_controller = app.controllers.login_user()
        return login_user_controller.execute(user)
