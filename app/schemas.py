from pydantic import BaseModel
from datetime import date
from typing import Union

class BookingBase(BaseModel):
    name: str  
    departure_date: date
    return_date: date
    departure_city: str
    arrival_city: str
    activities: Union[str, None] = None

class BookingCreate(BookingBase):
    pass

class Booking(BookingBase):
    id: int
    fk_user_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    name: str
    email: str
    birthdate: date
    gender: str
    telephone: str
    adress: str
    city: str
    postal_code: str
    country: str
    job: Union[str, None] = None
    company: Union[str, None] = None
    hobbies: Union[str, None] = None
    language: Union[str, None] = None
    topics: Union[str, None] = None
    notifications: Union[str, None] = None
    consent: Union[str, None] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    bookings: list[Booking] = []

    class Config:
        orm_mode = True
