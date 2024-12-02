from pydantic import BaseModel,Field
from typing import Optional
from bson import ObjectId

class Address(BaseModel):
    city: str = Field(..., min_length=2 , max_length=50)
    country: str = Field(...,min_length=2 , max_length=50)

class Student(BaseModel):
    id: Optional[str] = Field(None, alias = "_id")
    name: str = Field(...,min_length=2,max_length=50)
    age: int = Field(..., gt = 0,le=150)
    address: Address

    class Config:
        json_encoders =  {
            ObjectId: str
        }
        populate_by_name = True
        from_attributes = True