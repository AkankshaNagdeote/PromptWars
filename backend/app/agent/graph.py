import os
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from google import genai
from app.core.config import settings

# Setup Gemini Model via the unified Google GenAI SDK
# This SDK is optimized for May 2026 and supports Gemini 3 models
client = genai.Client(api_key=settings.google_api_key)
MODEL_NAME = "gemini-flash-latest" # Points to the current stable Flash model (Gemini 3/3.1)


# Problem Statement Alignment: Assistant for election process, timelines, and steps.
SYSTEM_PROMPT = """You are a highly knowledgeable Election Assistant.
Your objective is to help users understand the election process, timelines, and necessary steps in an interactive and easy-to-follow way.

Guidelines:
1. Provide accurate, clear, and concise information about elections.
2. Structure your responses with clear steps or timelines if applicable.
3. Be strictly neutral and unbiased. Do not endorse any political party or candidate.
4. If a user asks a question unrelated to the election process, politely redirect them back to the topic of elections.
"""

class AgentState(TypedDict):
    """
    State representing the ongoing conversation.
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]

def generate_response(state: AgentState):
    """
    Node function to call the Gemini 3 model and generate a response.
    """
    messages = state["messages"]
    
    # Format messages for the google-genai SDK
    # Role must be "user" or "model". System instructions go in config.
    prompt_messages = []
    
    for m in messages:
        if isinstance(m, SystemMessage):
            continue # System messages handled in config below
            
        role = "user" if isinstance(m, HumanMessage) else "model"
        prompt_messages.append({
            "role": role, 
            "parts": [{"text": m.content}]
        })
        
    try:
        # Call Gemini 3 via the new Client
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt_messages,
            config={
                "system_instruction": SYSTEM_PROMPT,
                "temperature": 0.3,
            }
        )
        
        return {"messages": [AIMessage(content=response.text)]}
    except Exception as e:
        # Proper error handling
        return {"messages": [AIMessage(content=f"I'm sorry, I encountered an error while processing your request: {str(e)}")]}

# Build LangGraph
graph_builder = StateGraph(AgentState)
graph_builder.add_node("agent", generate_response)
graph_builder.add_edge(START, "agent")
graph_builder.add_edge("agent", END)

# Compile graph
app_graph = graph_builder.compile()
