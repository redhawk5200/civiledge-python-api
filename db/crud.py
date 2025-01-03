from sqlalchemy.orm import Session
from .models import ChatSession
from datetime import datetime

def create_chat_session(db: Session, userid: str, langchain_thread_id: str, messages: str):
    chat_session = ChatSession(
        userid=userid,
        langchain_thread_id=langchain_thread_id,
        messages=messages,
        timestamp=datetime.utcnow()
    )
    db.add(chat_session)
    db.commit()
    db.refresh(chat_session)
    return chat_session

def get_chat_sessions(db: Session, userid: str):
    return db.query(ChatSession).filter(ChatSession.userid == userid).all()
