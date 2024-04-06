from fastapi import Depends, FastAPI, Form
from sqlalchemy.orm import Session

from database import engine
from dependencies.get_db import get_db
from services.api import webhook as webhook_service
from models import Base
Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.post("/webhooks/whatsapp/message")
def receive_message(Body: str = Form(), WaId: str = Form(),   db: Session = Depends(get_db)):
    data = {
        "webhook_data": {
            "message": Body,
            "wa_id": WaId
        },
        "db": db
    }
    return webhook_service.run_conversation_flow(**data)
