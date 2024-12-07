import jwt
from config import Config
from fastapi import status
from fastapi.responses import JSONResponse
from schemas import User
from services import DBService


class TokenController:
    def __init__(self, auth_service: DBService, config: Config) -> None:
        self.auth_service = auth_service
        self.config = config

    def execute(self, user: User) -> JSONResponse:
        data_to_encode = {
            'username': user.username,
            'email': user.email,
            'name': user.name,
            'lastname': user.lastname,
            'phone': user.phone
        }

        token = jwt.encode(data_to_encode, self.config.jwt_key,
                           self.config.jwt_algorithm)

        self.auth_service.set(user.user_id, token,
                              self.config.redis_expiration_mins)

        response = {'message': 'token created successfully'}
        return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)
