from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db

from .schemas import (
    CreateUserRequest,
    CurrentUserResponse,
    UpdateCurrentUserRequest,
    UpdateUserRequest,
    UserResponse,
)
from .service import (
    InvalidAccessTokenError,
    InvalidCurrentPasswordError,
    UserAlreadyExistsError,
    UserNotFoundError,
    create_system_user,
    delete_system_user,
    get_current_user_profile,
    get_system_user,
    list_system_users,
    update_system_user,
    update_current_user_profile,
)

users_router = APIRouter()
bearer_scheme = HTTPBearer(auto_error=False)


def get_access_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
    if not credentials:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Missing access token")

    if credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid auth scheme")

    return credentials.credentials


@users_router.get("/me", response_model=CurrentUserResponse)
def get_current_user(
    access_token: str = Depends(get_access_token),
    db: Session = Depends(get_db),
):
    try:
        return get_current_user_profile(db=db, access_token=access_token)
    except InvalidAccessTokenError as error:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=str(error)) from error
    except UserNotFoundError as error:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(error)) from error


@users_router.patch("/me", response_model=CurrentUserResponse)
def update_current_user(
    payload: UpdateCurrentUserRequest,
    access_token: str = Depends(get_access_token),
    db: Session = Depends(get_db),
):
    try:
        return update_current_user_profile(
            db=db,
            access_token=access_token,
            full_name=payload.full_name,
            current_password=payload.current_password,
            new_password=payload.new_password,
        )
    except InvalidAccessTokenError as error:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=str(error)) from error
    except InvalidCurrentPasswordError as error:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(error)) from error
    except UserNotFoundError as error:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(error)) from error


@users_router.get("/", response_model=list[UserResponse])
def get_users(
    access_token: str = Depends(get_access_token),
    db: Session = Depends(get_db),
):
    _ = access_token
    return list_system_users(db)


@users_router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    access_token: str = Depends(get_access_token),
    db: Session = Depends(get_db),
):
    _ = access_token
    try:
        return get_system_user(db, user_id)
    except UserNotFoundError as error:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(error)) from error


@users_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: CreateUserRequest,
    access_token: str = Depends(get_access_token),
    db: Session = Depends(get_db),
):
    _ = access_token
    try:
        return create_system_user(
            db=db,
            email=payload.email,
            full_name=payload.full_name,
            password=payload.password,
            is_active=payload.is_active,
            settings=payload.settings,
        )
    except UserAlreadyExistsError as error:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(error)) from error


@users_router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    payload: UpdateUserRequest,
    access_token: str = Depends(get_access_token),
    db: Session = Depends(get_db),
):
    _ = access_token
    try:
        return update_system_user(
            db=db,
            user_id=user_id,
            email=payload.email,
            full_name=payload.full_name,
            password=payload.password,
            is_active=payload.is_active,
            settings=payload.settings,
        )
    except UserNotFoundError as error:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(error)) from error
    except UserAlreadyExistsError as error:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(error)) from error


@users_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_user(
    user_id: int,
    access_token: str = Depends(get_access_token),
    db: Session = Depends(get_db),
):
    _ = access_token
    try:
        delete_system_user(db=db, user_id=user_id)
    except UserNotFoundError as error:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(error)) from error
