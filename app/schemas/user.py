from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    role: str

    class Config:
        orm_mode = True

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
