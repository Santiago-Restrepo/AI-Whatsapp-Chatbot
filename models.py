from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    country_code = Column(String)
    created_at = Column(DateTime)

    conversations = relationship("Conversation", back_populates="user")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    body = Column(String)
    response = Column(String)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    created_at = Column(DateTime)

    conversation = relationship("Conversation", back_populates="messages")
  
class Llm(Base):
    __tablename__ = "llms"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime)

    conversations = relationship("Conversation", back_populates="llm")

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    llm_id = Column(Integer, ForeignKey("llms.id"))
    created_at = Column(DateTime)

    user = relationship("User", back_populates="conversations")
    llm = relationship("Llm", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")