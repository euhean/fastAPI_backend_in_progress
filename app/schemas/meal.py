from pydantic import BaseModel


class MealBase(BaseModel):
    first: str
    second: str
    third: str
    beverage: str
    small_menu: bool
    allergies: str

class MealCreate(MealBase):
    pass

class Meal(MealBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True