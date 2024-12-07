import container
import uvicorn
from config import Config
from fastapi import FastAPI
from routes import router

config = Config()


def on_startup():
    container.AppContainer.init()


tags = [
    {
        'name': 'Health Check',
        'description': 'Describe the status of the application and its components.'
    },
    {
        'name': 'Auth',
        'description': 'Operations to manage authorization.'
    }
]

app = FastAPI(
    title='Auth',
    summary='Register tokens and validate tokens.',
    description='Service to create tokens.',
    openapi_tags=tags,
    on_startup=[on_startup]
)

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=config.port)
