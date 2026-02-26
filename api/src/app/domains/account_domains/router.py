from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db

from .models import AccountDomainName, AccountDomainStatus
from .schemas import (
    AccountDomainResponse,
    CreateAccountDomainRequest,
    UpdateAccountDomainRequest,
)
from .service import (
    AccountDomainAlreadyExistsError,
    AccountDomainNotFoundError,
    UnitNotFoundError,
    create_system_account_domain,
    delete_system_account_domain,
    get_system_account_domain,
    list_system_account_domains,
    update_system_account_domain,
)

account_domains_router = APIRouter()
bearer_scheme = HTTPBearer(auto_error=False)


def get_access_token(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> str:
    if not credentials:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Missing access token")

    if credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid auth scheme")

    return credentials.credentials


@account_domains_router.get("/", response_model=list[AccountDomainResponse])
def get_account_domains(
    search: str | None = Query(default=None, min_length=1, max_length=255),
    name: AccountDomainName | None = None,
    status_filter: AccountDomainStatus | None = Query(default=None, alias="status"),
    unit_id: int | None = Query(default=None, gt=0),
    access_token: str = Depends(get_access_token),
    db: Session = Depends(get_db),
):
    _ = access_token
    return list_system_account_domains(
        db=db,
        search=search,
        name=name,
        status=status_filter,
        unit_id=unit_id,
    )


@account_domains_router.get("/{account_domain_id}", response_model=AccountDomainResponse)
def get_account_domain(
    account_domain_id: int,
    access_token: str = Depends(get_access_token),
    db: Session = Depends(get_db),
):
    _ = access_token
    try:
        return get_system_account_domain(db=db, account_domain_id=account_domain_id)
    except AccountDomainNotFoundError as error:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(error)) from error


@account_domains_router.post(
    "/",
    response_model=AccountDomainResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_account_domain(
    payload: CreateAccountDomainRequest,
    access_token: str = Depends(get_access_token),
    db: Session = Depends(get_db),
):
    _ = access_token
    try:
        return create_system_account_domain(
            db=db,
            name=payload.name,
            login=payload.login,
            unit_id=payload.unit_id,
            status=payload.status,
            accesses=payload.accesses,
            ns_accounts=payload.ns_accounts,
        )
    except AccountDomainAlreadyExistsError as error:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(error)) from error
    except UnitNotFoundError as error:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(error)) from error
    except IntegrityError as error:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Failed to create account domain") from error


@account_domains_router.patch("/{account_domain_id}", response_model=AccountDomainResponse)
def update_account_domain(
    account_domain_id: int,
    payload: UpdateAccountDomainRequest,
    access_token: str = Depends(get_access_token),
    db: Session = Depends(get_db),
):
    _ = access_token
    try:
        return update_system_account_domain(
            db=db,
            account_domain_id=account_domain_id,
            name=payload.name,
            login=payload.login,
            unit_id=payload.unit_id,
            status=payload.status,
            accesses=payload.accesses,
            ns_accounts=payload.ns_accounts,
            update_unit_id="unit_id" in payload.model_fields_set,
        )
    except AccountDomainNotFoundError as error:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(error)) from error
    except AccountDomainAlreadyExistsError as error:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(error)) from error
    except UnitNotFoundError as error:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(error)) from error
    except IntegrityError as error:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Failed to update account domain") from error


@account_domains_router.delete("/{account_domain_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_account_domain(
    account_domain_id: int,
    access_token: str = Depends(get_access_token),
    db: Session = Depends(get_db),
):
    _ = access_token
    try:
        delete_system_account_domain(db=db, account_domain_id=account_domain_id)
    except AccountDomainNotFoundError as error:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(error)) from error

