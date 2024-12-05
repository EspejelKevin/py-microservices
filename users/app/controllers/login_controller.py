import re

from fastapi import status
from fastapi.responses import JSONResponse
from schemas import LoginUser
from services import DBService
from utils import Utils

PASSWORD_PATTERN = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$'


class LoginController:
    def __init__(self, user_service: DBService) -> None:
        self.user_service = user_service

    def execute(self, user: LoginUser) -> JSONResponse:
        response = {'message': 'user logged in successfully'}

        if not re.match(PASSWORD_PATTERN, user.password):
            response['message'] = 'invalid password due to format'
            return JSONResponse(content=response, status_code=status.HTTP_400_BAD_REQUEST)

        user_from_db = self.user_service.get(user.username)

        if not user_from_db:
            response['message'] = f'user <{user.username}> does not exist'
            return JSONResponse(content=response, status_code=status.HTTP_404_NOT_FOUND)

        if not Utils.verify_password(user.password, user_from_db.password):
            response['message'] = 'invalid password'
            return JSONResponse(content=response, status_code=status.HTTP_400_BAD_REQUEST)

        dummy_user = {
            'username': user_from_db.username,
            'email': user_from_db.email,
            'name': user_from_db.name,
            'lastname': user_from_db.lastname,
            'phone': user_from_db.phone
        }
        response['data'] = dummy_user

        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
