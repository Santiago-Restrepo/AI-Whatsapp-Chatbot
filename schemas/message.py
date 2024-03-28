from schemas.timestamp import TimestampBaseModel


class MessageBase(TimestampBaseModel):
    body: str
    response: str
    conversation_id: int


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: int

    class Config:
        orm_mode = True
