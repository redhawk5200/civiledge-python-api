from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
from datetime import datetime

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    id = Column(Integer, primary_key=True, index=True)
    userid = Column(String, nullable=False)
    langchain_thread_id = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    messages = Column(String, nullable=False)
