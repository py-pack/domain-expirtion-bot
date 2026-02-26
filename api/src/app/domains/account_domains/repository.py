from collections.abc import Sequence

from sqlalchemy import String, cast, func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.domains.units.models import Unit

from .models import AccountDomain, AccountDomainName, AccountDomainStatus, NsAccount


def list_account_domains(
    db: Session,
    *,
    search: str | None = None,
    name: AccountDomainName | None = None,
    status: AccountDomainStatus | None = None,
    unit_id: int | None = None,
) -> list[tuple[AccountDomain, str | None]]:
    statement = (
        select(AccountDomain, Unit.name)
        .outerjoin(Unit, Unit.id == AccountDomain.unit_id)
        .options(selectinload(AccountDomain.ns_accounts))
        .order_by(AccountDomain.id.asc())
    )

    if search:
        normalized_search_value = search.strip().lower()
        if normalized_search_value:
            normalized_search = f"%{normalized_search_value}%"
            statement = statement.where(
                or_(
                    func.lower(AccountDomain.login).like(normalized_search),
                    func.lower(cast(AccountDomain.name, String)).like(normalized_search),
                    func.lower(func.coalesce(Unit.name, "")).like(normalized_search),
                )
            )

    if name is not None:
        statement = statement.where(AccountDomain.name == name)

    if status is not None:
        statement = statement.where(AccountDomain.status == status)

    if unit_id is not None:
        statement = statement.where(AccountDomain.unit_id == unit_id)

    rows = db.execute(statement).all()
    return [(row[0], row[1]) for row in rows]


def get_account_domain_by_id(db: Session, account_domain_id: int) -> AccountDomain | None:
    statement = (
        select(AccountDomain)
        .options(selectinload(AccountDomain.ns_accounts))
        .where(AccountDomain.id == account_domain_id)
    )
    return db.execute(statement).scalar_one_or_none()


def get_account_domain_with_unit_by_id(
    db: Session, account_domain_id: int
) -> tuple[AccountDomain, str | None] | None:
    statement = (
        select(AccountDomain, Unit.name)
        .outerjoin(Unit, Unit.id == AccountDomain.unit_id)
        .options(selectinload(AccountDomain.ns_accounts))
        .where(AccountDomain.id == account_domain_id)
    )
    row = db.execute(statement).first()
    if row is None:
        return None

    return row[0], row[1]


def get_account_domain_by_name_login(
    db: Session,
    *,
    name: AccountDomainName,
    login: str,
) -> AccountDomain | None:
    statement = (
        select(AccountDomain)
        .where(AccountDomain.name == name, func.lower(AccountDomain.login) == login.lower())
        .limit(1)
    )
    return db.execute(statement).scalar_one_or_none()


def create_account_domain(db: Session, account_domain: AccountDomain) -> AccountDomain:
    db.add(account_domain)
    db.commit()
    db.refresh(account_domain)
    return account_domain


def save_account_domain(db: Session, account_domain: AccountDomain) -> AccountDomain:
    db.add(account_domain)
    db.commit()
    db.refresh(account_domain)
    return account_domain


def delete_account_domain(db: Session, account_domain: AccountDomain) -> None:
    db.delete(account_domain)
    db.commit()


def replace_ns_accounts(
    db: Session,
    *,
    account_domain: AccountDomain,
    ns_values: Sequence[str],
) -> None:
    account_domain.ns_accounts = [NsAccount(ns=value) for value in ns_values]
    db.add(account_domain)
    db.flush()
