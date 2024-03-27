from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    llm_id = Column(Integer, ForeignKey("llms.id"))
    created_at = Column(DateTime)

    user = relationship("User", back_populates="conversations")
    llm = relationship("Llm", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")