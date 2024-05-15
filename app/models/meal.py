from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from ..database import Base


class Meal(Base):
    __tablename__ = "meal"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    first = Column(String, nullable=False)
    second = Column(String, nullable=False)
    third = Column(String, nullable=False)
    beverage = Column(String, nullable=False)
    small_menu = Column(Boolean, nullable=False)
    allergies = Column(String)
    paid = Column(Boolean)

    user = relationship("User", back_populates="meals")
