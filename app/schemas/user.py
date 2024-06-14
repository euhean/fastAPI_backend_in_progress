from pydantic import BaseModel
from datetime import date
from . import Meal, Mail


class UserBase(BaseModel):
    name: str
    email: str
    birthdate: date
    telephone: str
    table: int
    paid: bool = False

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    meals: list[Meal] = []
    mails: list[Mail] = []

    class Config:
        orm_mode = True