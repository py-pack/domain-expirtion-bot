from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from .models import AccountDomainName, AccountDomainStatus


def _normalize_ns_values(values: list[str]) -> list[str]:
    normalized: list[str] = []
    seen: set[str] = set()

    for value in values:
        ns = value.strip()
        if not ns:
            raise ValueError("ns_accounts entries must not be empty")

        key = ns.lower()
        if key in seen:
            raise ValueError("ns_accounts entries must be unique")

        seen.add(key)
        normalized.append(ns)

    return normalized


class AccountDomainResponse(BaseModel):
    id: int
    name: AccountDomainName
    login: str
    unit_id: int | None
    unit_name: str | None
    status: AccountDomainStatus
    accesses: dict[str, Any]
    ns_accounts: list[str]
    created_at: datetime
    last_update_at: datetime


class CreateAccountDomainRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: AccountDomainName
    login: str = Field(min_length=1, max_length=255)
    unit_id: int | None = Field(default=None, gt=0)
    status: AccountDomainStatus = AccountDomainStatus.ACTIVE
    accesses: dict[str, Any] = Field(default_factory=dict)
    ns_accounts: list[str] = Field(default_factory=list)

    @field_validator("ns_accounts")
    @classmethod
    def validate_ns_accounts(cls, values: list[str]) -> list[str]:
        return _normalize_ns_values(values)


class UpdateAccountDomainRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: AccountDomainName | None = None
    login: str | None = Field(default=None, min_length=1, max_length=255)
    unit_id: int | None = Field(default=None, gt=0)
    status: AccountDomainStatus | None = None
    accesses: dict[str, Any] | None = None
    ns_accounts: list[str] | None = None

    @field_validator("ns_accounts")
    @classmethod
    def validate_ns_accounts(cls, values: list[str] | None) -> list[str] | None:
        if values is None:
            return None

        return _normalize_ns_values(values)

    @model_validator(mode="after")
    def validate_payload(self) -> "UpdateAccountDomainRequest":
        if self.model_fields_set == set():
            raise ValueError("At least one field must be provided")

        return self

