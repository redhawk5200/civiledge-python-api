from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime, timedelta
from pydantic import BaseModel
import asyncio
from zoneinfo import ZoneInfoNotFoundError
from tzlocal import get_localzone
import json
from fuzzywuzzy import process

from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
# from db.database import get_db, jobstores
# from schema.schema import ReminderCreate
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
    return get_openai_response("I was involved in a car accident last week. The other driver ran a red light and hit my car. I was injured and my car was damaged. I need help understanding my legal options.")


@app.post("/chat/", summary="Your Legal assistant powered with AI", description="Tell your case to the CivilEdge AI and it will respond to you with information needed to further access your case.")
async def chat_with_assistant(user_input: UserInput):
    return {"response": "You should file a lawsuit"}
    