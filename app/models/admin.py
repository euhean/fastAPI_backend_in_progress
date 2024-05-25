from sqlalchemy import Column, Integer, String, DateTime
from ..database import Base


class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    birthdate = Column(DateTime, nullable=False)
    password = Column(String, nullable=False)