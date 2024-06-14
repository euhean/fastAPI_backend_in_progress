from pydantic import BaseModel


class MailBase(BaseModel):
    subject: str
    body: str


class MailCreate(MailBase):
    pass


class Mail(MailBase):
    id: int
    user_id: int
    sent: bool = False

    class Config:
        orm_mode = True