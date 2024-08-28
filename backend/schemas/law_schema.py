from pydantic import BaseModel

class LawBase(BaseModel):
    title: str
    content: str

class LawCreate(LawBase):
    pass

class LawResponse(LawBase):
    id: int

    class Config:
        orm_mode = True