# main.py  (local: uvicorn main:app --reload --host 0.0.0.0 --port 8000)
import os
import secrets
from typing import Optional

from fastapi import FastAPI, Depends, Header, HTTPException
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

# Clave de administrador: se define como variable de entorno (ADMIN_KEY) en Render.
# Si no está definida, los endpoints de borrado rechazan todas las peticiones.
ADMIN_KEY = os.environ.get("ADMIN_KEY")


def verificar_admin(x_admin_key: Optional[str] = Header(None)):
    if (
        not ADMIN_KEY
        or not x_admin_key
        or not secrets.compare_digest(x_admin_key.encode(), ADMIN_KEY.encode())
    ):
        raise HTTPException(status_code=401, detail="No autorizado")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/lecturas", response_model=schemas.LecturaOut)
def crear_lectura(lectura: schemas.LecturaCreate, db: Session = Depends(get_db)):
    nueva = models.Lectura(**lectura.model_dump())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva


@app.get("/lecturas", response_model=list[schemas.LecturaOut])
def listar_lecturas(limit: int = 50, db: Session = Depends(get_db)):
    return db.query(models.Lectura).order_by(models.Lectura.id.desc()).limit(limit).all()


@app.delete("/lecturas", dependencies=[Depends(verificar_admin)])
def vaciar_lecturas(db: Session = Depends(get_db)):
    """Borra TODAS las lecturas. Requiere el header x-admin-key."""
    borradas = db.query(models.Lectura).delete()
    db.commit()
    return {"borradas": borradas}


@app.delete("/lecturas/nodo/{node_id}", dependencies=[Depends(verificar_admin)])
def vaciar_nodo(node_id: int, db: Session = Depends(get_db)):
    """Borra solo las lecturas de un nodo. Requiere el header x-admin-key."""
    borradas = (
        db.query(models.Lectura)
        .filter(models.Lectura.node_id == node_id)
        .delete()
    )
    db.commit()
    return {"borradas": borradas, "node_id": node_id}
