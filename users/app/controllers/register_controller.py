import re

from fastapi import status
from fastapi.responses import JSONResponse
from schemas import RegisterUser
from services import DBService
from utils import Utils

PASSWORD_PATTERN = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$'


class RegisterController:
    def __init__(self, user_service: DBService) -> None:
        self.user_service = user_service

    def execute(self, user: RegisterUser) -> JSONResponse:
        response = {'message': 'user created successfully'}

        if not re.match(PASSWORD_PATTERN, user.password):
            response['message'] = 'invalid password due to format'
            return JSONResponse(content=response, status_code=status.HTTP_400_BAD_REQUEST)

        user_from_db = self.user_service.get(user.username)

        if user_from_db:
            response['message'] = f'user with username <{
                user.username}> already exists'
            return JSONResponse(content=response, status_code=status.HTTP_409_CONFLICT)

        user.password = Utils.hash_password(user.password)

        success = self.user_service.save(user)

        if not success:
            response['message'] = f'errro while saving user <{user.username}>'
            return JSONResponse(content=response, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)
