from sqlalchemy.orm import Session

from models.user import User
from schemas.user import UserCreate

def get_user_by_phone(db: Session, phone: str):
    return db.query(User).filter(User.phone == phone).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user_if_not_exists(db: Session, phone: str):
    user = get_user_by_phone(db, phone)
    if user:
        return user
    user = UserCreate(phone=phone, name="", created_at="2024-03-27T02:07:46.200Z'")
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
