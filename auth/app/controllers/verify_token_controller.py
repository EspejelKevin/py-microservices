import jwt
from config import Config
from fastapi import status
from fastapi.responses import JSONResponse
from schemas import User
from services import DBService


class VerifyTokenController:
    def __init__(self, auth_service: DBService, config: Config) -> None:
        self.auth_service = auth_service
        self.config = config

    def execute(self, credentials: str) -> JSONResponse:
        response = {
            'message': 'unauthorized user, invalid o expired credentials'}
        token = self.auth_service.get(credentials)

        if not token:
            return JSONResponse(content=response, status_code=status.HTTP_401_UNAUTHORIZED)

        try:
            payload = jwt.decode(token, self.config.jwt_key,
                                 self.config.jwt_algorithm)
        except Exception:
            return JSONResponse(content=response, status_code=status.HTTP_401_UNAUTHORIZED)

        response['message'] = 'valid token'
        response['data'] = payload

        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
