from datetime import datetime, UTC
from typing import Optional

from fastapi import Body, Request, Response, APIRouter, Depends, HTTPException
from jose import JWTError
from sqlalchemy.orm import Session

from app.infra.jwt.google_service import verify_google_token, get_user_email_from_google
from .service import login_for_tokens, login_verified_user, decode_jwt, get_token, delete_token
from .schemas import LoginRequest, GoogleLoginRequest, GoogleCallbackRequest, TokenPair, RefreshRequest

from app.core.database import get_db
from app.core.config import settings

auth_router = APIRouter()
REFRESH_COOKIE_NAME = "refresh_token"


def _is_secure_request(request: Request) -> bool:
    forwarded_proto = request.headers.get("x-forwarded-proto")
    if forwarded_proto:
        return forwarded_proto.lower() == "https"

    return request.url.scheme == "https"


def _set_refresh_cookie(response: Response, request: Request, refresh_token: str) -> None:
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=refresh_token,
        httponly=True,
        secure=_is_secure_request(request),
        samesite="lax",
        path="/api/v1/auth",
    )


def _clear_refresh_cookie(response: Response, request: Request) -> None:
    response.delete_cookie(
        key=REFRESH_COOKIE_NAME,
        path="/api/v1/auth",
        secure=_is_secure_request(request),
        samesite="lax",
    )


def _resolve_refresh_token(data: Optional[RefreshRequest], request: Request) -> str:
    token_from_body = data.refresh_token if data else None
    token = token_from_body or request.cookies.get(REFRESH_COOKIE_NAME)

    if not token:
        raise HTTPException(401, "Refresh token is missing")

    return token


def _extract_refresh_token(token_pair: dict) -> str:
    refresh_token = token_pair.get("refresh_token")
    if not isinstance(refresh_token, str) or not refresh_token:
        raise HTTPException(500, "Refresh token generation failed")

    return refresh_token


@auth_router.post("/login", response_model=TokenPair)
def login(
    payload: LoginRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    user_agent = request.headers.get("user-agent")
    token_pair = login_for_tokens(db, str(payload.email), payload.password, user_agent)
    _set_refresh_cookie(response, request, _extract_refresh_token(token_pair))
    return token_pair


@auth_router.post("/login-google", response_model=TokenPair)
def google_callback(
    payload: GoogleCallbackRequest,
    request: Request,
    response: Response,
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

        token_pair = login_verified_user(db, verify_result.get('email'), user_agent)
        _set_refresh_cookie(response, request, _extract_refresh_token(token_pair))
        return token_pair
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@auth_router.post("/login-google-one-tap", response_model=TokenPair)
async def google_login(
    payload: GoogleLoginRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    user_agent = request.headers.get("user-agent")
    try:
        verify_result = verify_google_token(payload.id_token, settings.google.client_id)
        token_pair = login_verified_user(db, verify_result.get('email'), user_agent)
        _set_refresh_cookie(response, request, _extract_refresh_token(token_pair))
        return token_pair

    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


@auth_router.post("/refresh", response_model=TokenPair)
async def refresh_token(
    request: Request,
    response: Response,
    data: RefreshRequest | None = Body(default=None),
    db: Session = Depends(get_db),
):
    user_agent = request.headers.get("user-agent")
    refresh_token_value = _resolve_refresh_token(data, request)

    try:
        payload = decode_jwt(refresh_token_value)
    except JWTError:
        raise HTTPException(401, "Invalid token")

    if payload.get('type') != "refresh":
        raise HTTPException(401, "Wrong token type")

    if datetime.now(UTC).timestamp() > payload.get('exp'):
        raise HTTPException(401, "Token expired")

    db_token = get_token(db, refresh_token_value)
    if not db_token:
        raise HTTPException(401, "Token not found")
    delete_token(db, refresh_token_value, payload.get('sid'))

    email = payload.get('email')
    if not isinstance(email, str) or not email:
        raise HTTPException(401, "Invalid token payload")
    token_pair = login_verified_user(db, email, user_agent)
    _set_refresh_cookie(response, request, _extract_refresh_token(token_pair))
    return token_pair


@auth_router.post("/logout")
def logout(
    request: Request,
    response: Response,
    payload: RefreshRequest | None = Body(default=None),
    db: Session = Depends(get_db),
):
    token = _resolve_refresh_token(payload, request)
    payload_jwt = decode_jwt(token)
    delete_token(db, token, payload_jwt.get('sid'))
    _clear_refresh_cookie(response, request)
    return {"detail": "Successfully logged out"}
