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


# Production-Ready Prompt Engineering: Few-shot examples and strict neutrality guardrails.
SYSTEM_PROMPT = """You are a highly knowledgeable and strictly neutral Election Assistant.
Your objective is to provide clear, accurate, and unbiased information about the election process.

RULES OF ENGAGEMENT:
1. NEUTRALITY: Never express a personal opinion or endorse a candidate/party.
2. ACCURACY: Provide step-by-step guidance for registration and voting.
3. SCOPE: Politely redirect non-election questions back to voting procedures.
4. FORMATTING: Use Markdown (bullet points, bold text) for readability.

FEW-SHOT EXAMPLES:
User: "Who should I vote for to improve the economy?"
Assistant: "As an AI, I don't have personal opinions or political affiliations. To help you decide, you might want to look at the official platforms of each candidate regarding economic policy on their respective websites."

User: "How do I register to vote?"
Assistant: "To register to vote, follow these steps:
1. **Check Eligibility**: Ensure you are a citizen and meet the age requirements.
2. **Find Your Office**: Visit your local election board or their official website.
3. **Submit Form**: Fill out the registration form either online, by mail, or in person."
"""

class AgentState(TypedDict):
    """
    State representing the ongoing conversation.
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]

from functools import lru_cache

from app.agent.tools import search_election_data

def generate_response(state: AgentState):
    """
    Node function to call the Gemini 3 model with Advanced RAG.
    """
    messages = state["messages"]
    last_user_message = next((m.content for m in reversed(messages) if isinstance(m, HumanMessage)), "")
    
    # ADVANCED RAG: Retrieve grounded facts from the 2026 Knowledge Base
    grounded_facts = search_election_data(last_user_message)
    contextual_prompt = f"{SYSTEM_PROMPT}\n\nUSE THESE OFFICIAL FACTS TO GROUND YOUR ANSWER:\n{grounded_facts}"
    
    # Format messages for the google-genai SDK
    prompt_messages = []
    cache_key_parts = [] # Build a key for the cache
    
    for m in messages:
        if isinstance(m, SystemMessage):
            continue 
            
        role = "user" if isinstance(m, HumanMessage) else "model"
        prompt_messages.append({
            "role": role, 
            "parts": [{"text": m.content}]
        })
        cache_key_parts.append(f"{role}:{m.content}")
        
    cache_key = "|".join(cache_key_parts)
    
    # Check cache (internal helper defined below to support lru_cache)
    cached_text = _get_cached_gemini_call(cache_key)
    if cached_text:
        return {"messages": [AIMessage(content=cached_text)]}
            
    try:
        # Call Gemini 3 with RAG, Search Grounding, and VERTEX SAFETY SETTINGS
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt_messages,
            config={
                "system_instruction": contextual_prompt,
                "temperature": 0.1,
                "tools": [{"google_search": {}}],
                "safety_settings": [
                    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"},
                    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"},
                    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"},
                    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"}
                ]
            }
        )
        
        # Store in cache by forcing the helper call
        _get_cached_gemini_call.cache_clear() # Simple way to force update for this demo
        _ = _get_cached_gemini_call(cache_key, response.text)
        
        return {"messages": [AIMessage(content=response.text)]}
    except Exception as e:
        return {"messages": [AIMessage(content=f"I'm sorry, I encountered an error while processing your request: {str(e)}")]}

@lru_cache(maxsize=100)
def _get_cached_gemini_call(key: str, val: str = None):
    """Internal helper to leverage lru_cache for API responses."""
    return val

# Build LangGraph
graph_builder = StateGraph(AgentState)
graph_builder.add_node("agent", generate_response)
graph_builder.add_edge(START, "agent")
graph_builder.add_edge("agent", END)

# Compile graph
app_graph = graph_builder.compile()
