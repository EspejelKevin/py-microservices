from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    name: str
    lastname: str
    phone: str
    user_id: str
