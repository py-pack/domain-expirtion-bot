from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from infra.jwt.google_service import verify_google_token, exchange_code_for_token, get_user_email_from_google
from .service import login_for_tokens, login_user_by_email
from .schemas import LoginRequest, GoogleLoginRequest, GoogleCallbackRequest

from src.database import get_db
from settings import settings

auth_router = APIRouter()


@auth_router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return login_for_tokens(db, str(payload.email), payload.password)


@auth_router.post("/login-google")
def google_callback(payload: GoogleCallbackRequest, db: Session = Depends(get_db)):
    try:
        verify_result = get_user_email_from_google(
            payload.code,
            settings.google.client_id,
            settings.google.client_secret,
            settings.google.redirect_uri
        )

        return login_user_by_email(db, verify_result.get('email'))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@auth_router.post("/login-google-one-tap")
async def google_login(payload: GoogleLoginRequest, db: Session = Depends(get_db)):
    try:
        verify_result = verify_google_token(payload.id_token, settings.google.client_id)
        return login_user_by_email(db, verify_result.get('email'))

    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
