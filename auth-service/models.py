from pydantic import BaseModel

class LoginUser(BaseModel):
    email: str
    password: str

class User(BaseModel):
    email: str
    name: str
    password: str

class ProfileUpdateUser(BaseModel):
    email: str | None = None
    name: str | None = None
    password: str | None = None
