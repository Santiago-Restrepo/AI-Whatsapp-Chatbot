from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database import Base

class Llm(Base):
    __tablename__ = "llms"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime)

    conversations = relationship("Conversation", back_populates="llm")
