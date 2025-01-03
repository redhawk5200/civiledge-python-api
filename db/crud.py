from sqlalchemy.orm import Session
from .models import ChatSession
from datetime import datetime
import json

def create_new_chat_session(db: Session, userid: str, langchain_thread_id: str, messages: str):
    """Create a new chat session."""
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

def append_chat_session(db: Session, userid: str, langchain_thread_id: str, messages: str):
    """
    Check if the user and thread ID exist in the database. 
    If yes, append messages to the current session. 
    Otherwise, create a new chat session.
    """
    # Check for an existing chat session
    existing_session = db.query(ChatSession).filter(
        ChatSession.userid == userid,
        ChatSession.langchain_thread_id == langchain_thread_id
    ).first()
    
    if existing_session:
        # Parse the existing messages
        existing_messages = json.loads(existing_session.messages)
        # Parse the new messages
        new_messages = json.loads(messages)
        print("\n==========================================\n")
        print ("existing messages", existing_messages)
        print ("new messages", new_messages)

        # Ensure existing_messages and new_messages are lists
        if isinstance(existing_messages, list) and isinstance(new_messages, list):
            # Merge the messages
            updated_messages = json.dumps(existing_messages['response'].append(new_messages['response'][:-1]))
        else:
            raise ValueError("Messages must be lists for appending.")

        print("\n==========================================\n")
        print ("\n\nexisting messages", existing_messages)
        print ("new messages", new_messages)

        # Update the session with merged messages
        existing_session.messages = updated_messages
        existing_session.timestamp = datetime.utcnow()
        db.commit()
        db.refresh(existing_session)
        return existing_session
    else:
        # Create a new chat session if no existing session found
        return create_new_chat_session(db, userid, langchain_thread_id, messages)


def get_chat_sessions(db: Session, userid: str):
    return db.query(ChatSession).filter(ChatSession.userid == userid).all()

def delete_chat_session(db: Session, userid: str):
    db.query(ChatSession).filter(ChatSession.userid == userid).delete()
    db.commit()
    return

def delete_all_chat_sessions(db: Session):
    db.query(ChatSession).delete()
    db.commit()
    return

