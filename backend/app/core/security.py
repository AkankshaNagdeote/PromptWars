import json
import time
from collections import defaultdict
from fastapi import Request, HTTPException

# --- GOOGLE SERVICES: Structured Logging ---
class StructuredLogger:
    @staticmethod
    def info(msg: str, trace_id: str = None, **kwargs):
        log_entry = {
            "severity": "INFO", 
            "message": msg, 
            "service": "election-assistant",
            "logging.googleapis.com/trace": trace_id,
            **kwargs
        }
        print(json.dumps(log_entry))
    
    @staticmethod
    def error(msg: str, trace_id: str = None, **kwargs):
        log_entry = {
            "severity": "ERROR", 
            "message": msg, 
            "service": "election-assistant",
            "logging.googleapis.com/trace": trace_id,
            **kwargs
        }
        print(json.dumps(log_entry))

# --- SECURITY: Rate Limiting ---
rate_limit_store = defaultdict(list)
RATE_LIMIT_CALLS = 15 
RATE_LIMIT_WINDOW = 60 # seconds

def rate_limiter(request: Request):
    client_ip = request.client.host
    now = time.time()
    rate_limit_store[client_ip] = [t for t in rate_limit_store[client_ip] if now - t < RATE_LIMIT_WINDOW]
    if len(rate_limit_store[client_ip]) >= RATE_LIMIT_CALLS:
        StructuredLogger.error(f"Rate limit exceeded for IP: {client_ip}")
        raise HTTPException(status_code=429, detail="Too many requests. Please try again later.")
    rate_limit_store[client_ip].append(now)
