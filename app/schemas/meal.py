from pydantic import BaseModel
from typing import Union


class MealBase(BaseModel):
    first: str
    second: str
    third: str
    beverage: str
    small_menu: bool
    allergies: Union[str, None]


class MealCreate(MealBase):
    pass


class Meal(MealBase):
    id: int
    user_id: int
    paid: bool = False

    class Config:
        orm_mode = True