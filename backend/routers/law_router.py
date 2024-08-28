from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.law import Law
from models.chat_history import ChatHistory  # Import model ChatHistory
from schemas.law_schema import LawCreate, LawResponse
from database.database import SessionLocal
from services.chatbot_service import get_chatbot_response
from pydantic import BaseModel

router = APIRouter()

# Dependency untuk mendapatkan session database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Question(BaseModel):
    question: str

@router.post("/ask")
async def ask_question(question: Question, db: Session = Depends(get_db)):
    # Menggunakan layanan chatbot untuk mendapatkan respons
    answer = get_chatbot_response(question.question)

    # Simpan riwayat ke database
    chat_history = ChatHistory(question=question.question, answer=answer)
    db.add(chat_history)
    db.commit()
    db.refresh(chat_history)

    return {"question": question.question, "answer": answer}

@router.get("/history")
async def get_history(db: Session = Depends(get_db)):
    history = db.query(ChatHistory).all()
    return history

@router.post("/laws", response_model=LawResponse)
async def create_law(law: LawCreate, db: Session = Depends(get_db)):
    db_law = Law(title=law.title, content=law.content)
    db.add(db_law)
    db.commit()
    db.refresh(db_law)
    return db_law

@router.get("/laws/{law_id}", response_model=LawResponse)
async def read_law(law_id: int, db: Session = Depends(get_db)):
    db_law = db.query(Law).filter(Law.id == law_id).first()
    if db_law is None:
        raise HTTPException(status_code=404, detail="Law not found")
    return db_law

@router.delete("/clear_history")
async def clear_history(db: Session = Depends(get_db)):
    db.query(ChatHistory).delete()
    db.commit()
    return {"message": "Riwayat chat berhasil dihapus."}