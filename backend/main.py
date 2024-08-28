# law-ai/backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import law_router
from database.database import engine, Base  # Impor engine dan Base
import warnings

warnings.filterwarnings("ignore")

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ganti dengan URL frontend Anda jika perlu
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Buat tabel di database
Base.metadata.create_all(bind=engine)

app.include_router(law_router.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to AI Hakim API"}