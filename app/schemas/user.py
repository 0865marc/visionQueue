from pydantic import BaseModel, EmailStr

class LoginUser(BaseModel):
    email: EmailStr
    password: str

class CreateUser(LoginUser):
    username: str