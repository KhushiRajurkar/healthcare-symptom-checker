from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from llm_handler import analyze_symptoms
from database import SymptomEntry, SessionLocal

app = FastAPI(title="Healthcare Symptom Checker", version="2.0")

# ---- CORS (keep your original setup)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Pydantic model
class SymptomInput(BaseModel):
    text: str

# ---- Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---- Analyze route (logs into DB)
@app.post("/analyze")
async def analyze(input: SymptomInput, db: Session = Depends(get_db)):
    result = analyze_symptoms(input.text)

    entry = SymptomEntry(
        symptoms=input.text,
        result=result,
        model_used="Groq LLaMA 3.1"
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)

    return {"result": result}

# ---- History route (view saved entries)
@app.get("/history")
async def get_history(
    keyword: str | None = Query(None, description="Filter by symptom or condition keyword"),
    db: Session = Depends(get_db)
):
    query = db.query(SymptomEntry).order_by(SymptomEntry.timestamp.desc())

    if keyword:
        pattern = f"%{keyword.lower()}%"
        query = query.filter(
            (SymptomEntry.symptoms.ilike(pattern)) | (SymptomEntry.result.ilike(pattern))
        )

    entries = query.all()
    return [
        {
            "id": e.id,
            "symptoms": e.symptoms,
            "result": e.result,
            "model": e.model_used,
            "timestamp": e.timestamp
        }
        for e in entries
    ]

@app.delete("/history/{entry_id}")
async def delete_entry(entry_id: int):
    db = SessionLocal()
    entry = db.query(SymptomEntry).filter(SymptomEntry.id == entry_id).first()
    if not entry:
        db.close()
        raise HTTPException(status_code=404, detail="Entry not found")
    db.delete(entry)
    db.commit()
    db.close()
    return {"message": f"Entry {entry_id} deleted successfully"}

@app.delete("/history")
async def delete_all_history():
    db = SessionLocal()
    db.query(SymptomEntry).delete()
    db.commit()
    db.close()
    return {"message": "All history deleted successfully"}

# ---- Root route
@app.get("/")
async def root():
    return {"message": "Welcome to the Healthcare Symptom Checker API"}
