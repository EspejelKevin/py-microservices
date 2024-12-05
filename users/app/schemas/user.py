from pydantic import BaseModel, Field

PATTERN_EMAIL = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
PATTERN_PHONE = r'^\+52\s1[0-9]{10}$'


class RegisterUser(BaseModel):
    username: str = Field(min_length=5, max_length=30)
    password: str = Field(min_length=8)
    email: str = Field(max_length=100, pattern=PATTERN_EMAIL)
    phone: str = Field(pattern=PATTERN_PHONE)
    name: str = Field(min_length=1, max_length=50)
    lastname: str = Field(min_length=1, max_length=50)


class LoginUser(BaseModel):
    username: str = Field(min_length=5, max_length=30)
    password: str = Field(min_length=8)
