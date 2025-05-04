from typing import Type

from sqlalchemy.orm import Session
from .models import User


def get_user_by_email(db: Session, email: str) -> Type[User] | None:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
