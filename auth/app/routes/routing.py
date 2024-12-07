import container
from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from schemas import User

router = APIRouter(prefix='/api/v1/auth')


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


@router.post('/token', tags=['Auth'])
def get_token(user: User) -> JSONResponse:
    with container.AppContainer.scope() as app:
        token_controller = app.controllers.token()
        return token_controller.execute(user)


@router.get('/identity', tags=['Auth'])
def verify_token(authorization: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> JSONResponse:
    with container.AppContainer.scope() as app:
        verify_token_controller = app.controllers.verify_token()
        return verify_token_controller.execute(authorization.credentials)
