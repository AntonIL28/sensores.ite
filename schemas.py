# schemas.py
from pydantic import BaseModel
from datetime import datetime

class LecturaCreate(BaseModel):
    node_id: int
    temperatura: float
    humedad: float

class LecturaOut(LecturaCreate):
    id: int
    timestamp: datetime
    class Config:
        from_attributes = True