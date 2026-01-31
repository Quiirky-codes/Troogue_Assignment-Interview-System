# fastapi_service/models.py
import os
from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey, Text, Float, Boolean)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "interviewdb")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{quote_plus(POSTGRES_PASSWORD)}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

Base = declarative_base()

class Interview(Base):
    __tablename__ = "interviews"
    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer)
    skill = Column(String(100))
    status = Column(String(50))
    started_at = Column(DateTime)
    completed_at = Column(DateTime)

class InterviewQuestion(Base):
    __tablename__ = "interview_questions"
    id = Column(Integer, primary_key=True)
    skill = Column(String(100))
    text = Column(Text)
    expected_keywords = Column(Text)

class InterviewAnswer(Base):
    __tablename__ = "interview_answers"
    id = Column(Integer, primary_key=True)
    interview_id = Column(Integer)
    question_id = Column(Integer)
    answer_text = Column(Text)
    uploaded_file_path = Column(String(1024))
    scored = Column(Boolean)
    score = Column(Float)
    evaluator_notes = Column(Text)

class InterviewResult(Base):
    __tablename__ = "interview_results"
    id = Column(Integer, primary_key=True)
    interview_id = Column(Integer)
    total_score = Column(Float)
    verdict = Column(String(50))
    details = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
