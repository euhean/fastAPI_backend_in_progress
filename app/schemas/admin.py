from pydantic import BaseModel
from datetime import date


class AdminBase(BaseModel):
    name: str
    email: str
    birthdate: date
    
    class Config:
        orm_mode = True


class AdminCreate(AdminBase):
    password: str


class Admin(AdminBase):
    id: str