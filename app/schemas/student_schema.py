from pydantic import BaseModel, Field
from typing import Optional
from app.models.student import Address

class StudentCreate(BaseModel):
    name: str = Field(...,min_length=2 ,max_length=50)
    age: int = Field(... ,gt = 0,le = 150)
    address:Address

class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None , min_length=2, max_length = 50)
    age: Optional[int] = Field(None , gt = 0,le = 150)
    address: Optional[Address] = None