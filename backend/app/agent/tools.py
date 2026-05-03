import json
import os

# Path to the knowledge base relative to this file
KNOWLEDGE_BASE_PATH = os.path.join(os.path.dirname(__file__), "knowledge_base.json")

def search_election_data(query: str) -> str:
    """
    Search the official 2026 Election Knowledge Base for specific laws and timelines.
    Use this when the user asks for registration details, ID laws, or specific dates.
    """
    try:
        with open(KNOWLEDGE_BASE_PATH, "r") as f:
            data = json.load(f)
        
        # Simple keyword-based RAG retrieval
        matches = []
        query_lower = query.lower()
        for item in data:
            if query_lower in item["topic"].lower() or any(word in item["content"].lower() for word in query_lower.split()):
                matches.append(f"TOPIC: {item['topic']}\nFACT: {item['content']}")
        
        if not matches:
            return "No specific official facts found for this query in the 2026 database."
            
        return "\n\n".join(matches)
    except Exception as e:
        return f"Error retrieving data: {str(e)}"
