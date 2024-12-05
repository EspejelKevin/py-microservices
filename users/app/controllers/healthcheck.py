from fastapi.responses import JSONResponse
from services import DBService


class HealthChekController:
    def __init__(self, user_service: DBService) -> None:
        self.user_service = user_service

    def liveness(self) -> JSONResponse:
        return JSONResponse(content={'status': 'ok'})

    def readiness(self) -> JSONResponse:
        data = self.user_service.is_up()
        response = {'message': 'MySQL is up'}

        if not data['success']:
            response['message'] = 'MySQL is down'

        return JSONResponse(content=response)
