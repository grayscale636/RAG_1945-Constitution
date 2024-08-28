# law-ai/backend/models/law.py
from sqlalchemy import Column, Integer, String
from database.database import Base  # Pastikan ini diimpor setelah Base didefinisikan

class Law(Base):
    __tablename__ = "laws"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)