import pyodbc
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Ticket Data API")

# Enable CORS (for React frontend to call this)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can replace * with specific origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB credentials (from .env or hardcoded — update accordingly)
DB_USER = os.getenv("DB_USER", "voiceadmin")
DB_PASS = os.getenv("DB_PASS", "Voice@dm!n")
DB_SERVER = os.getenv("DB_SERVER", "july-hackathon.database.windows.net")
DB_NAME = os.getenv("DB_NAME", "voice_nba")

# Connection string
connection_string = (
    f'DRIVER={{ODBC Driver 18 for SQL Server}};'
    f'SERVER=tcp:{DB_SERVER},1433;'
    f'DATABASE={DB_NAME};'
    f'UID={DB_USER};'
    f'PWD={DB_PASS};'
    'Encrypt=yes;'
    'TrustServerCertificate=no;'
)

@app.get("/api/tickets")
def get_tickets():
    try:
        with pyodbc.connect(connection_string) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ticket_number, 
                       creation_date, 
                       current_Status, 
                       assigned_to, 
                       priority, 
                       subject, 
                       any_other_comments 
                FROM voice_nba.dbo.voice_tickets;
            """)
            columns = [column[0] for column in cursor.description]
            tickets = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return tickets
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {str(e)}")

@app.get("/health")
def health():
    return {"status": "ok"}



# import logging
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from typing import List, Optional
# import os
# from dotenv import load_dotenv
# load_dotenv()

# # Logging setup
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Import the isolated agent logic
# from .sk_agent import SemanticKernelAgent


# app = FastAPI(title="Multi-Agent Semantic Kernel Chat API")

# # Pydantic models
# class ChatRequest(BaseModel):
#     user: str
#     message: str



# agent = SemanticKernelAgent()

# @app.post("/chat")
# async def chat(request: ChatRequest):
#     try:
#         response = await agent.chat(request.user, request.message)
#         return response
#     except Exception as e:
#         logger.error(f"Chat error: {e}")
#         #raise HTTPException(status_code=500, detail="Chat agent error.")
#         raise HTTPException(status_code=500, detail=f"Chat error: {e}")


# # Health check endpoint
# @app.get("/health")
# def health():
#     return {"status": "ok"}

# # Health check endpoint
# @app.get("/ticket")
# def ticket():
#     return {"status": "ok"}

