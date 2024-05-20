from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from ..database import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    birthdate = Column(DateTime, nullable=False)
    password = Column(String, nullable=False)
    telephone = Column(String, unique=True, nullable=False)
    table = Column(Integer, nullable=False)
    paid = Column(Boolean)

    meals = relationship("Meal", back_populates="user")