from pydantic import BaseModel
from datetime import date


class AdminBase(BaseModel):
    name: str
    email: str
    birthdate: date


class AdminCreate(AdminBase):
    password: str


class Admin(AdminBase):
    id: str

    class Config:
        orm_mode = True