from pydantic import BaseModel

class TimestampBaseModel(BaseModel):
    created_at: str

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

class UserBase(TimestampBaseModel):
    phone: str
    country_code: str
    name: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    conversations: list[Conversation] = []

    class Config:
        orm_mode = True


class LlmBase(TimestampBaseModel):
    name: str

class LlmCreate(LlmBase):
    pass

class Llm(LlmBase):
    id: int
    conversations: list[Conversation] = []

    class Config:
        orm_mode = True

