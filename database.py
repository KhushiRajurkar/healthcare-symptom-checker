from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Create SQLite engine
engine = create_engine("sqlite:///symptom_history.db", echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

# Table definition
class SymptomEntry(Base):
    __tablename__ = "symptom_history"
    id = Column(Integer, primary_key=True, index=True)
    symptoms = Column(Text)
    result = Column(Text)
    model_used = Column(String(100))
    timestamp = Column(DateTime, default=datetime.utcnow)

# Create table if it doesn't exist
Base.metadata.create_all(engine)
