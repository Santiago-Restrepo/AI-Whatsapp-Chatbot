from schemas.timestamp import TimestampBaseModel
from schemas.message import Message
from datetime import datetime
class ConversationBase(TimestampBaseModel):
    user_id: int
    llm_id: int
    active: bool
    started_at: datetime | None

class ConversationCreate(ConversationBase):
    pass

class Conversation(ConversationBase):
    id: int
    messages: list[Message] = []

    class Config:
        orm_mode = True