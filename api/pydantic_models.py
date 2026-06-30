from dotenv import load_dotenv
load_dotenv()
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

class ModelName(str, Enum):
    NEMOTRON     = "nvidia/nemotron-3-ultra-550b-a55b:free"
    GEMINI_FLASH = "google/gemini-2.0-flash-exp:free"
    LLAMA_3B     = "meta-llama/llama-3.2-3b-instruct:free"
    MISTRAL_7B   = "mistralai/mistral-7b-instruct:free"

class QueryInput(BaseModel):
    question: str
    session_id: str = Field(default=None)
    model: ModelName = Field(default=ModelName.NEMOTRON)

class QueryResponse(BaseModel):
    answer: str
    session_id: str
    model: ModelName

class DocumentInfo(BaseModel):
    id: int
    filename: str
    upload_timestamp: datetime

class DeleteFileRequest(BaseModel):
    file_id: int