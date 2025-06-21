from datetime import datetime, UTC
from fastapi import Request, APIRouter, Depends, HTTPException, Body
from jose import JWTError
from sqlalchemy.orm import Session

from infra.jwt.google_service import verify_google_token, get_user_email_from_google
from .service import login_for_tokens, login_user_by_email, decode_jwt, get_token, delete_token, create_token
from .schemas import LoginRequest, GoogleLoginRequest, GoogleCallbackRequest, TokenPair, RefreshRequest

from src.database import get_db
from settings import settings

auth_router = APIRouter()


@auth_router.post("/login", response_model=TokenPair)
def login(
        payload: LoginRequest,
        request: Request,
        db: Session = Depends(get_db),
):
    user_agent = request.headers.get("user-agent")
    return login_for_tokens(db, str(payload.email), payload.password, payload.session_id, user_agent)


@auth_router.post("/login-google", response_model=TokenPair)
def google_callback(
        payload: GoogleCallbackRequest,
        request: Request,
        db: Session = Depends(get_db),
):
    user_agent = request.headers.get("user-agent")
    try:
        verify_result = get_user_email_from_google(
            payload.code,
            settings.google.client_id,
            settings.google.client_secret,
            settings.google.redirect_uri
        )

        return login_user_by_email(db, verify_result.get('email'), payload.session_id, user_agent)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@auth_router.post("/login-google-one-tap", response_model=TokenPair)
async def google_login(
        payload: GoogleLoginRequest,
        request: Request,
        db: Session = Depends(get_db),
):
    user_agent = request.headers.get("user-agent")
    try:
        verify_result = verify_google_token(payload.id_token, settings.google.client_id)
        return login_user_by_email(db, verify_result.get('email'), payload.session_id, user_agent)

    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


@auth_router.post("/refresh", response_model=TokenPair)
async def refresh_token(
        data: RefreshRequest,
        request: Request,
        db: Session = Depends(get_db),
):
    user_agent = request.headers.get("user-agent")
    try:
        payload = decode_jwt(data.refresh_token)
    except JWTError:
        raise HTTPException(401, "Invalid token")

    if payload.get('type') != "refresh":
        raise HTTPException(401, "Wrong token type")

    if datetime.now(UTC).timestamp() > payload.get('exp'):
        raise HTTPException(401, "Token expired")

    db_token = get_token(db, data.refresh_token)
    if not db_token:
        raise HTTPException(401, "Token not found")
    delete_token(db, data.refresh_token)

    email = payload.get('sub')
    return login_user_by_email(db, email, data.session_id, user_agent)
