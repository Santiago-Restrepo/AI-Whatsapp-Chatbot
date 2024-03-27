from schemas.timestamp import TimestampBaseModel
from schemas.message import Message
class ConversationBase(TimestampBaseModel):
    user_id: int
    llm_id: int    

class ConversationCreate(ConversationBase):
    pass

class Conversation(ConversationBase):
    id: int
    messages: list[Message] = []

    class Config:
        orm_mode = True