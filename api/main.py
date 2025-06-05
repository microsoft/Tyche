
import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
load_dotenv()

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import the isolated agent logic
from .sk_agent import SemanticKernelAgent


app = FastAPI(title="Multi-Agent Semantic Kernel Chat API")

# Pydantic models
class ChatRequest(BaseModel):
    user: str
    message: str



agent = SemanticKernelAgent()

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        response = await agent.chat(request.user, request.message)
        return response
    except Exception as e:
        logger.error(f"Chat error: {e}")
        #raise HTTPException(status_code=500, detail="Chat agent error.")
        raise HTTPException(status_code=500, detail=f"Chat error: {e}")


# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}

