from datetime import UTC, datetime
from typing import Any

from sqlalchemy.orm import Session

from app.domains.units.repository import get_unit_by_id

from .models import (
    AccountDomain,
    AccountDomainDetails,
    AccountDomainListItem,
    AccountDomainName,
    AccountDomainStatus,
)
from .repository import (
    create_account_domain,
    delete_account_domain,
    get_account_domain_by_id,
    get_account_domain_by_name_login,
    get_account_domain_with_unit_by_id,
    list_account_domains,
    replace_ns_accounts,
    save_account_domain,
)


class AccountDomainsDomainError(Exception):
    pass


class AccountDomainNotFoundError(AccountDomainsDomainError):
    pass


class AccountDomainAlreadyExistsError(AccountDomainsDomainError):
    pass


class UnitNotFoundError(AccountDomainsDomainError):
    pass


def _normalize_login(login: str) -> str:
    return login.strip()


def _normalize_accesses(accesses: dict[str, Any] | None) -> dict[str, Any]:
    return {} if accesses is None else accesses


def _normalize_ns_accounts(ns_accounts: list[str] | None) -> list[str]:
    if ns_accounts is None:
        return []

    normalized: list[str] = []
    seen: set[str] = set()

    for raw_value in ns_accounts:
        value = raw_value.strip()
        if not value:
            raise ValueError("ns_accounts entries must not be empty")

        key = value.lower()
        if key in seen:
            raise ValueError("ns_accounts entries must be unique")

        seen.add(key)
        normalized.append(value)

    return normalized


def _ensure_unit_exists(db: Session, unit_id: int | None) -> None:
    if unit_id is None:
        return

    if not get_unit_by_id(db, unit_id):
        raise UnitNotFoundError("Unit not found")


def _build_list_item(account: AccountDomain, unit_name: str | None) -> AccountDomainListItem:
    return AccountDomainListItem(
        id=account.id,
        name=account.name,
        login=account.login,
        unit_id=account.unit_id,
        unit_name=unit_name,
        status=account.status,
        accesses=dict(account.accesses or {}),
        ns_accounts=[row.ns for row in account.ns_accounts],
        created_at=account.created_at,
        last_update_at=account.last_update_at,
    )


def _build_details(account: AccountDomain, unit_name: str | None) -> AccountDomainDetails:
    return AccountDomainDetails(
        id=account.id,
        name=account.name,
        login=account.login,
        unit_id=account.unit_id,
        unit_name=unit_name,
        status=account.status,
        accesses=dict(account.accesses or {}),
        ns_accounts=[row.ns for row in account.ns_accounts],
        created_at=account.created_at,
        last_update_at=account.last_update_at,
    )


def list_system_account_domains(
    db: Session,
    *,
    search: str | None = None,
    name: AccountDomainName | None = None,
    status: AccountDomainStatus | None = None,
    unit_id: int | None = None,
) -> list[AccountDomainListItem]:
    rows = list_account_domains(
        db,
        search=search,
        name=name,
        status=status,
        unit_id=unit_id,
    )
    return [_build_list_item(account, unit_name) for account, unit_name in rows]


def get_system_account_domain(db: Session, account_domain_id: int) -> AccountDomainDetails:
    row = get_account_domain_with_unit_by_id(db, account_domain_id)
    if row is None:
        raise AccountDomainNotFoundError("Account domain not found")

    account, unit_name = row
    return _build_details(account, unit_name)


def create_system_account_domain(
    db: Session,
    *,
    name: AccountDomainName,
    login: str,
    unit_id: int | None,
    status: AccountDomainStatus,
    accesses: dict[str, Any] | None,
    ns_accounts: list[str] | None,
) -> AccountDomainDetails:
    normalized_login = _normalize_login(login)
    if not normalized_login:
        raise ValueError("Login is required")

    _ensure_unit_exists(db, unit_id)

    if get_account_domain_by_name_login(db, name=name, login=normalized_login):
        raise AccountDomainAlreadyExistsError("Account domain with same provider and login already exists")

    account_domain = AccountDomain(
        name=name,
        login=normalized_login,
        unit_id=unit_id,
        status=status,
        accesses=_normalize_accesses(accesses),
        last_update_at=datetime.now(UTC),
    )
    replace_ns_accounts(
        db,
        account_domain=account_domain,
        ns_values=_normalize_ns_accounts(ns_accounts),
    )
    created = create_account_domain(db, account_domain)
    created_row = get_account_domain_with_unit_by_id(db, created.id)
    if created_row is None:
        raise AccountDomainNotFoundError("Account domain not found")
    return _build_details(created_row[0], created_row[1])


def update_system_account_domain(
    db: Session,
    *,
    account_domain_id: int,
    name: AccountDomainName | None = None,
    login: str | None = None,
    unit_id: int | None = None,
    status: AccountDomainStatus | None = None,
    accesses: dict[str, Any] | None = None,
    ns_accounts: list[str] | None = None,
    update_unit_id: bool = False,
) -> AccountDomainDetails:
    account_domain = get_account_domain_by_id(db, account_domain_id)
    if not account_domain:
        raise AccountDomainNotFoundError("Account domain not found")

    if update_unit_id:
        _ensure_unit_exists(db, unit_id)
        account_domain.unit_id = unit_id

    if name is not None:
        account_domain.name = name

    if login is not None:
        normalized_login = _normalize_login(login)
        if not normalized_login:
            raise ValueError("Login is required")
        account_domain.login = normalized_login

    if status is not None:
        account_domain.status = status

    if accesses is not None:
        account_domain.accesses = _normalize_accesses(accesses)

    if ns_accounts is not None:
        replace_ns_accounts(
            db,
            account_domain=account_domain,
            ns_values=_normalize_ns_accounts(ns_accounts),
        )

    duplicate = get_account_domain_by_name_login(
        db,
        name=account_domain.name,
        login=account_domain.login,
    )
    if duplicate and duplicate.id != account_domain.id:
        raise AccountDomainAlreadyExistsError("Account domain with same provider and login already exists")

    account_domain.last_update_at = datetime.now(UTC)
    save_account_domain(db, account_domain)

    row = get_account_domain_with_unit_by_id(db, account_domain_id)
    if row is None:
        raise AccountDomainNotFoundError("Account domain not found")

    return _build_details(row[0], row[1])


def delete_system_account_domain(db: Session, account_domain_id: int) -> None:
    account_domain = get_account_domain_by_id(db, account_domain_id)
    if not account_domain:
        raise AccountDomainNotFoundError("Account domain not found")

    delete_account_domain(db, account_domain)
