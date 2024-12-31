from dotenv import load_dotenv
from core.config import get_config
from schema.schemas import User
from fastapi import FastAPI
from typing import List
from uuid import uuid4

load_dotenv()

app = FastAPI()

db: List[User]= [
    User(
        id=uuid4(),
        conversation_id=uuid4(),
        name="John Doe",
        email="john@gmail.com",
        is_active=True
    ),
    User(
        id=uuid4(),
        conversation_id=uuid4(),
        name="Mary Doe",
        email="mary@gmail.com",
        is_active=False
    )
]

@app.get("/")
async def root():
    return {"Hello": "Mundo"}

@app.get("/api/v1/users")
async def fetch_users():
    return db



# config = get_config()
# print(config)
