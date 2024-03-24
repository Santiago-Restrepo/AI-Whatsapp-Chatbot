from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import models, services
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
def receive_message(body, db: Session = Depends(get_db)):
    return services.receive_whatsapp_message(db, body)