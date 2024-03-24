from sqlalchemy.orm import Session

from models import User
from schemas import UserCreate
from clients.twilio import client

def receive_whatsapp_message(db: Session, body: str, wa_id: str):
    
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body='You said: {}'.format(body),
        to='whatsapp:+{}'.format(wa_id)
    )

    return {"message_id": message.sid}  # Return only the message ID


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
