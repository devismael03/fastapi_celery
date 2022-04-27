from pydantic import BaseModel

class UserDto(BaseModel):
    username: str
    password: str

class TaskDto(BaseModel):
    ip: str
    city: str
    country: str