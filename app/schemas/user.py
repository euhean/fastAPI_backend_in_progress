from pydantic import BaseModel
from datetime import date
from meal import Meal


class UserBase(BaseModel):
    name: str
    email: str
    birthdate: date
    telephone: str
    table: str
    paid = False

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    meals: list[Meal] = []

    class Config:
        orm_mode = True