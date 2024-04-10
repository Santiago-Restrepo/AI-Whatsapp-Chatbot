from schemas.timestamp import TimestampBaseModel
from schemas.conversation import Conversation


class UserBase(TimestampBaseModel):
    phone: str
    name: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    conversations: list[Conversation] = []

    class Config:
        orm_mode = True
