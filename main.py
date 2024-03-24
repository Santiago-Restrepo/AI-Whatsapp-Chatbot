from fastapi import Depends, FastAPI, HTTPException, Form
from sqlalchemy.orm import Session

import models, services, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
#V75ZCPZUAEQ92JB34YPGJ2B5

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/webhooks/whatsapp/message")
def receive_message(Body: str = Form(), WaId: str = Form(),   db: Session = Depends(get_db)):

    response = services.receive_whatsapp_message(db, Body.lower(), WaId)
    return response