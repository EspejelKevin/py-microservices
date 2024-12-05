import container
import uvicorn
from fastapi import FastAPI
from routes import router


def on_startup():
    container.AppContainer.init()


tags = [
    {
        'name': 'Health Check',
        'description': 'Describe the status of the application and its components.'
    },
    {
        'name': 'Users',
        'description': 'Operations to manage users.'
    }
]

app = FastAPI(
    title='Users',
    summary='Register accounts and Login.',
    description='Service to create accounts and login.',
    openapi_tags=tags,
    on_startup=[on_startup]
)

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0')
