from fastapi import FastAPI, Depends, HTTPException
from . import crud, models, schemas
from .database import SessionLocal, engine


models.Base.metadata.create_all(engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": 'Hello world!'}
