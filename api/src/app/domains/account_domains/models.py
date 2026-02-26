from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class AccountDomainName(str, Enum):
    UKRAINE_HOST = "ukraine_host"
    NAME_CHEAP = "name_cheap"
    GO_DADDY = "go_daddy"
    WHOIS = "whois"
    CLOUD_FLARE = "cloud_flare"


class AccountDomainStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    WARNING = "warning"
    BAN = "ban"


class AccountDomain(Base):
    __tablename__ = "account_domains"
    __table_args__ = (
        UniqueConstraint("name", "login", name="uq_account_domains_name_login"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[AccountDomainName] = mapped_column(
        SqlEnum(
            AccountDomainName,
            name="account_domain_name",
            values_callable=lambda enum_cls: [item.value for item in enum_cls],
        ),
        nullable=False,
        index=True,
    )
    login: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    unit_id: Mapped[int | None] = mapped_column(
        ForeignKey("units.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    accesses: Mapped[dict[str, object]] = mapped_column(JSONB, nullable=False, default=dict)
    status: Mapped[AccountDomainStatus] = mapped_column(
        SqlEnum(
            AccountDomainStatus,
            name="account_domain_status",
            values_callable=lambda enum_cls: [item.value for item in enum_cls],
        ),
        nullable=False,
        default=AccountDomainStatus.ACTIVE,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )
    last_update_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    ns_accounts: Mapped[list["NsAccount"]] = relationship(
        back_populates="account_domain",
        cascade="all, delete-orphan",
        passive_deletes=True,
        order_by="NsAccount.id",
    )


class NsAccount(Base):
    __tablename__ = "ns_accounts"
    __table_args__ = (
        UniqueConstraint("account_id", "ns", name="uq_ns_accounts_account_ns"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(
        ForeignKey("account_domains.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    ns: Mapped[str] = mapped_column(String(255), nullable=False)

    account_domain: Mapped[AccountDomain] = relationship(back_populates="ns_accounts")


@dataclass(frozen=True)
class AccountDomainListItem:
    id: int
    name: AccountDomainName
    login: str
    unit_id: int | None
    unit_name: str | None
    status: AccountDomainStatus
    accesses: dict[str, object]
    ns_accounts: list[str]
    created_at: datetime
    last_update_at: datetime


@dataclass(frozen=True)
class AccountDomainDetails:
    id: int
    name: AccountDomainName
    login: str
    unit_id: int | None
    unit_name: str | None
    status: AccountDomainStatus
    accesses: dict[str, object]
    ns_accounts: list[str]
    created_at: datetime
    last_update_at: datetime

