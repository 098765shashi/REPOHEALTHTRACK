from typing import Any, Optional, List
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class AnalyzeRequest(BaseModel):
    url: str
    branch: str = "main"

class RepoOut(BaseModel):
    id: int
    url: str
    name: str
    branch: str
    status: str
    health_score: float
    created_at: datetime
    updated_at: datetime
    error: Optional[str] = None
    class Config: from_attributes = True

class MetricsOut(BaseModel):
    repo_id: int
    metrics: dict
    ai_report: Optional[str] = None
