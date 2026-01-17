from datetime import datetime, UTC
from fastapi import Request, APIRouter, Depends, HTTPException
from jose import JWTError
from sqlalchemy.orm import Session

from app.infra.jwt.google_service import verify_google_token, get_user_email_from_google
from .service import login_for_tokens, login_verified_user, decode_jwt, get_token, delete_token
from .schemas import LoginRequest, GoogleLoginRequest, GoogleCallbackRequest, TokenPair, RefreshRequest

from app.core.database import get_db
from app.core.config import settings

auth_router = APIRouter()


@auth_router.post("/login", response_model=TokenPair)
def login(
    payload: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    user_agent = request.headers.get("user-agent")
    return login_for_tokens(db, str(payload.email), payload.password, user_agent)


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

        return login_verified_user(db, verify_result.get('email'), user_agent)
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
        return login_verified_user(db, verify_result.get('email'), user_agent)

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
    delete_token(db, data.refresh_token, payload.get('sid'))

    email = payload.get('sub')
    return login_verified_user(db, email, user_agent)


@auth_router.post("/logout")
def logout(
    payload: RefreshRequest,
    db: Session = Depends(get_db),
):
    payload_jwt = decode_jwt(payload.refresh_token)
    delete_token(db, payload.refresh_token, payload_jwt.get('sid'))
    return {"detail": "Successfully logged out"}
