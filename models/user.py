from sqlalchemy import Column, Integer, String, DateTime
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
