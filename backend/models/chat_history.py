# law-ai/backend/models/chat_history.py
from sqlalchemy import Column, Integer, String
from database.database import Base  # Pastikan ini diimpor setelah Base didefinisikan

class ChatHistory(Base):
    __tablename__ = 'chat_history'

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, index=True)
    answer = Column(String)