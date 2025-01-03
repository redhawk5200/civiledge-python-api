from datetime import datetime, timedelta
from pydantic import BaseModel
import asyncio
from zoneinfo import ZoneInfoNotFoundError
import json

from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from db.database import get_db
from sqlalchemy.orm import Session
from schema.schemas import UserInput
from service.service import get_openai_response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health", summary="Health Check", description="Check if the server is running.")
async def health_check():
    return {"status": "healthy"}

@app.post("/chat/", summary="Your Legal assistant powered with AI", description="Tell your case to the CivilEdge AI and it will respond to you with information needed to further access your case.")
async def chat_with_assistant(user_input: UserInput, db: Session = Depends(get_db)):
    try:
        response = get_openai_response(user_input.message, user_input.userid)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
        {"response": "You should file a lawsuit"}    