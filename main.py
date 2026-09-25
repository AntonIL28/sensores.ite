# main.py uvicorn main:app --reload --host 0.0.0.0 --port 8000
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import models, schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/lecturas", response_model=schemas.LecturaOut)
def crear_lectura(lectura: schemas.LecturaCreate, db: Session = Depends(get_db)):
    nueva = models.Lectura(**lectura.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@app.get("/lecturas", response_model=list[schemas.LecturaOut])
def listar_lecturas(limit: int = 50, db: Session = Depends(get_db)):
    return db.query(models.Lectura).order_by(models.Lectura.id.desc()).limit(limit).all()