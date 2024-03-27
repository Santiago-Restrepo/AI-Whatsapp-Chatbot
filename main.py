from fastapi import Depends, FastAPI, HTTPException, Form
from sqlalchemy.orm import Session

from database import engine
from dependencies.get_db import get_db
from services.webhook import receive_whatsapp_message
from models import Base

Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.post("/webhooks/whatsapp/message")
def receive_message(Body: str = Form(), WaId: str = Form(),   db: Session = Depends(get_db)):

    response = receive_whatsapp_message(db, Body.lower(), WaId)
    return response