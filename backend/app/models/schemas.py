from pydantic import BaseModel, Field
from typing import List, Optional

class ChatRequest(BaseModel):
    """
    Schema for incoming chat requests.
    Includes type hints and field validations for code quality.
    """
    message: str = Field(..., description="The user's input message")
    session_id: str = Field(default="default_session", description="Unique session ID for conversation history")

class ChatResponse(BaseModel):
    """
    Schema for outgoing chat responses.
    """
    response: str = Field(..., description="The agent's reply")
    session_id: str = Field(..., description="The session ID")
    error: Optional[str] = Field(None, description="Error message if any")
