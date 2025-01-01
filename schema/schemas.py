from pydantic import BaseModel
from typing import Optional, Dict, Any, ClassVar
from uuid import UUID, uuid4

#Schema for userinput coming from frontend
class UserInput(BaseModel):
    prompt: str

# Schema for request
class QueryRequest(BaseModel):
    query: str
    conversation_id: Optional[UUID] = uuid4()
    class Config:
        json_schema_extra = {
            "example": {
                "query": "What is the weather today?",
                "conversation_id": "60b62e44-63b2-4c23-8968-3b443fcf0777"
            }
        }

# Schema for response
class QueryResponse(BaseModel):
    conversation_id: UUID
    response: Dict[str, Any] 
    class Config:
        json_schema_extra: ClassVar = {
            "examples": [
                {
                    "conversation_id": "60b62e44-63b2-4c23-8968-3b443fcf0777",
                    "response": {
                        "answer": "You should file a lawsuit"
                    }
                },
                {
                    "conversation_id": "a1b2c3d4-5678-9101-1121-314151617181",
                    "response": {
                        "plan": "Get on a call with an attorney"
                    }
                }
            ]
        }

#Schema for a user
class User(BaseModel):
    user_id: Optional[UUID] = uuid4()
    conversation_id: Optional[UUID] = uuid4()
    name: str
    email: str
    is_active: bool

