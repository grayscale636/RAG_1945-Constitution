from pydantic import BaseModel

class ChatHistoryResponse(BaseModel):
    id: int
    question: str
    answer: str

    class Config:
        orm_mode = True