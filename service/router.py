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

        print(response)

        # Extract the last message (AIMessage object)
        last_message = response["messages"][-1]

        # Check if a tool call exists in additional_kwargs
        if hasattr(last_message, "additional_kwargs"):
            tool_calls = last_message.additional_kwargs.get("tool_calls", [])
            if tool_calls and isinstance(tool_calls, list):
                first_tool_call = tool_calls[0]
                arguments = first_tool_call.get("function", {}).get("arguments", "")
                if arguments:
                    try:
                        # Parse the arguments as JSON
                        parsed_arguments = json.loads(arguments)
                        tool_report = parsed_arguments.get("convo")
                        if tool_report:
                            return {"response": tool_report}
                    except json.JSONDecodeError:
                        print("Error decoding JSON arguments:", arguments)

        # Default to returning the content of the last AIMessage
        if hasattr(last_message, "content"):
            return {"response": last_message.content or "No relevant response found."}

        # Fallback response
        return {"response": "No relevant response found."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
