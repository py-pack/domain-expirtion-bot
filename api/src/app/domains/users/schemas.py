from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator
from app.domains.units.models import UnitResponsibleLevel


class CurrentUserResponse(BaseModel):
    id: int
    email: str
    full_name: str


class UpdateCurrentUserRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    full_name: str = Field(min_length=1, max_length=255)
    current_password: Optional[str] = Field(default=None, min_length=1)
    new_password: Optional[str] = Field(default=None, min_length=8)

    @model_validator(mode="after")
    def validate_password_change(self) -> "UpdateCurrentUserRequest":
        has_current_password = bool(self.current_password)
        has_new_password = bool(self.new_password)

        if has_current_password != has_new_password:
            raise ValueError(
                "Both current_password and new_password must be provided to change password",
            )

        return self


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    is_active: bool
    settings: dict[str, Any]


class UserUnitAssignmentResponse(BaseModel):
    unit_id: int
    unit_name: str
    level: UnitResponsibleLevel


class UserUnitAssignmentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    unit_id: int = Field(gt=0)
    level: UnitResponsibleLevel


class ReplaceUserUnitAssignmentsRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    assignments: list[UserUnitAssignmentRequest] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_unique_units(self) -> "ReplaceUserUnitAssignmentsRequest":
        unit_ids = [assignment.unit_id for assignment in self.assignments]
        if len(set(unit_ids)) != len(unit_ids):
            raise ValueError("assignments.unit_id must be unique")
        return self


class CreateUserRequest(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=8)
    is_active: bool = True
    settings: dict[str, Any] = Field(default_factory=dict)


class UpdateUserRequest(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    password: Optional[str] = Field(default=None, min_length=8)
    is_active: Optional[bool] = None
    settings: Optional[dict[str, Any]] = None

    @model_validator(mode="after")
    def validate_update_payload(self) -> "UpdateUserRequest":
        has_any_value = any(
            [
                self.email is not None,
                self.full_name is not None,
                self.password is not None,
                self.is_active is not None,
                self.settings is not None,
            ]
        )

        if not has_any_value:
            raise ValueError("At least one field must be provided")

        return self
