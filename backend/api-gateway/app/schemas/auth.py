from pydantic import BaseModel, EmailStr, Field


class UserCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)


class LoginSchema(BaseModel):
    email: EmailStr
    password: str
