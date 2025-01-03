import os
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager

# Configure database
DB_FILE = "sqlite_database.db"
if not os.path.exists(DB_FILE):
    open(DB_FILE, 'a').close()

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DB_FILE}")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Configure session and base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Job scheduling
jobstores = {
    'default': SQLAlchemyJobStore(url=DATABASE_URL)
}

def get_db():
    """Create a new database session and close it after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def db_session():
    """Provide a transactional scope around a series of operations."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# Import models
from .models import ChatSession

# Create database tables
Base.metadata.create_all(bind=engine)
