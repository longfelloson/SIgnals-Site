from pydantic import BaseModel, EmailStr, Field


class AccessToken(BaseModel):
    access_token: str
    token_type_: str


class RegisterUser(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLoginCredentials(BaseModel):
    email: EmailStr
    password: str


class UserCredentials(BaseModel):
    email: EmailStr
    username: str
    hashed_password: bytes


class CreateUser(BaseModel):
    email: EmailStr
    username: str
    hashed_password: bytes
