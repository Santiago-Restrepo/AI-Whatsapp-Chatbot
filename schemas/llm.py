from schemas.timestamp import TimestampBaseModel
from schemas.conversation import Conversation

class LlmBase(TimestampBaseModel):
    name: str

class LlmCreate(LlmBase):
    pass

class Llm(LlmBase):
    id: int
    conversations: list[Conversation] = []

    class Config:
        orm_mode = True

