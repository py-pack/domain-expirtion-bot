from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db

from .schemas import (
    CreateUnitRequest,
    ReplaceUnitResponsiblesRequest,
    UnitDetailsResponse,
    UnitResponsibleUserResponse,
    UnitResponse,
    UpdateUnitRequest,
)
from .service import (
    UnitAlreadyExistsError,
    UnitNotFoundError,
    UnitResponsibleUsersNotFoundError,
    create_system_unit,
    delete_system_unit,
    get_system_unit,
    list_system_unit_responsibles,
    list_system_units,
    replace_system_unit_responsibles,
    update_system_unit,
)

units_router = APIRouter()
bearer_scheme = HTTPBearer(auto_error=False)


def get_access_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
    if not credentials:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Missing access token")

    if credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid auth scheme")

    return credentials.credentials


@units_router.get("/", response_model=list[UnitResponse])
def get_units(
    access_token: str = Depends(get_access_token),
    db: Session = Depends(get_db),
):
    _ = access_token
    return list_system_units(db)


@units_router.get("/{unit_id}", response_model=UnitDetailsResponse)
def get_unit(
    unit_id: int,
    access_token: str = Depends(get_access_token),
    db: Session = Depends(get_db),
):
    _ = access_token
    try:
        return get_system_unit(db, unit_id)
    except UnitNotFoundError as error:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(error)) from error


@units_router.post("/", response_model=UnitDetailsResponse, status_code=status.HTTP_201_CREATED)
def create_unit(
    payload: CreateUnitRequest,
    access_token: str = Depends(get_access_token),
    db: Session = Depends(get_db),
):
    _ = access_token
    try:
        return create_system_unit(db=db, name=payload.name)
    except UnitAlreadyExistsError as error:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(error)) from error


@units_router.patch("/{unit_id}", response_model=UnitDetailsResponse)
def update_unit(
    unit_id: int,
    payload: UpdateUnitRequest,
    access_token: str = Depends(get_access_token),
    db: Session = Depends(get_db),
):
    _ = access_token
    try:
        return update_system_unit(db=db, unit_id=unit_id, name=payload.name)
    except UnitNotFoundError as error:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(error)) from error
    except UnitAlreadyExistsError as error:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(error)) from error


@units_router.delete("/{unit_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_unit(
    unit_id: int,
    access_token: str = Depends(get_access_token),
    db: Session = Depends(get_db),
):
    _ = access_token
    try:
        delete_system_unit(db=db, unit_id=unit_id)
    except UnitNotFoundError as error:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(error)) from error


@units_router.get("/{unit_id}/responsibles", response_model=list[UnitResponsibleUserResponse])
def get_unit_responsibles(
    unit_id: int,
    access_token: str = Depends(get_access_token),
    db: Session = Depends(get_db),
):
    _ = access_token
    try:
        return list_system_unit_responsibles(db=db, unit_id=unit_id)
    except UnitNotFoundError as error:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(error)) from error


@units_router.put("/{unit_id}/responsibles", response_model=list[UnitResponsibleUserResponse])
def put_unit_responsibles(
    unit_id: int,
    payload: ReplaceUnitResponsiblesRequest,
    access_token: str = Depends(get_access_token),
    db: Session = Depends(get_db),
):
    _ = access_token
    try:
        return replace_system_unit_responsibles(
            db=db,
            unit_id=unit_id,
            assignments=[assignment.model_dump(mode="json") for assignment in payload.assignments],
        )
    except UnitNotFoundError as error:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(error)) from error
    except UnitResponsibleUsersNotFoundError as error:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(error)) from error
