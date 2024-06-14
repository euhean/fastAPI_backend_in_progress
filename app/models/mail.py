from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class Mail(Base):
    __tablename__ = "mail"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    subject = Column(String, index=True)
    body = Column(String, index=True)
    sent = Column(Boolean, default=False)

    user = relationship("User", back_populates="mails")