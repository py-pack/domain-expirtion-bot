from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from .service import login_for_tokens, login_user_by_email
from .google_service import exchange_code_for_token, get_user_email_from_google
from .schemas import LoginRequest, GoogleCallbackRequest

auth_router = APIRouter()


@auth_router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return login_for_tokens(db, str(data.email), data.password)


@auth_router.post("/google-login")
def google_callback(data: GoogleCallbackRequest, db: Session = Depends(get_db)):
    try:
        access_token = exchange_code_for_token(data.code)
        email = get_user_email_from_google(access_token)

        return login_user_by_email(db, email)  # повертає access + refresh
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
