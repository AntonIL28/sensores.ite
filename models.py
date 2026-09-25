# models.py
from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime
from database import Base

class Lectura(Base):
    __tablename__ = "lecturas"
    id = Column(Integer, primary_key=True, index=True)
    node_id = Column(Integer, index=True)
    temperatura = Column(Float)
    humedad = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)