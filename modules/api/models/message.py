from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from modules.api.dependencies.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    body = Column(String)
    response = Column(String)
    conversation_id = Column(Integer, ForeignKey("conversations.id"))
    created_at = Column(DateTime)

    conversation = relationship("Conversation", back_populates="messages")
