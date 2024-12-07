from fastapi.responses import JSONResponse
from services import DBService


class HealthChekController:
    def __init__(self, auth_service: DBService) -> None:
        self.auth_service = auth_service

    def liveness(self) -> JSONResponse:
        return JSONResponse(content={'status': 'ok'})

    def readiness(self) -> JSONResponse:
        data = self.auth_service.is_up()
        response = {'message': 'Redis is up'}

        if not data['success']:
            response['message'] = 'Redis is down'

        return JSONResponse(content=response)
