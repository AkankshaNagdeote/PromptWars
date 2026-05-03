import logging
from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import ChatRequest, ChatResponse
from app.agent.graph import app_graph
from langchain_core.messages import HumanMessage

from app.core.security import rate_limiter, StructuredLogger

router = APIRouter()
sessions = {}

@router.post("/chat", response_model=ChatResponse, dependencies=[Depends(rate_limiter)])
async def chat_endpoint(request: ChatRequest) -> ChatResponse:
    """
    Main chat endpoint to interact with the Election Assistant agent.
    """
    StructuredLogger.info(f"Received chat request for session {request.session_id}")
    
    try:
        # Initialize session state if it doesn't exist
        if request.session_id not in sessions:
            sessions[request.session_id] = {"messages": []}
            
        state = sessions[request.session_id]
        state["messages"].append(HumanMessage(content=request.message))
        
        # Invoke LangGraph
        result = await app_graph.ainvoke(state)
        
        # Update session state with the result
        sessions[request.session_id] = result
        
        # Get the latest AI message
        ai_response = result["messages"][-1].content
        
        return ChatResponse(
            response=ai_response,
            session_id=request.session_id
        )
    except Exception as e:
        StructuredLogger.error(f"Error processing chat: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while processing the request.")
