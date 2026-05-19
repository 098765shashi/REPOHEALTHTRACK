from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text, JSON
from sqlalchemy.orm import relationship
from db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Repository(Base):
    __tablename__ = "repositories"
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    name = Column(String, nullable=False)
    branch = Column(String, default="main")
    status = Column(String, default="pending")  # pending|analyzing|done|error
    error = Column(Text, nullable=True)
    health_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metrics = Column(JSON, default=dict)
    ai_report = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
