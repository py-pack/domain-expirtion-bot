from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator
from .models import UnitResponsibleLevel


class UnitResponse(BaseModel):
    id: int
    name: str
    responsibles_count: int = 0


class UnitDetailsResponse(BaseModel):
    id: int
    name: str


class UnitResponsibleUserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    level: UnitResponsibleLevel


class CreateUnitRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=255)


class UpdateUnitRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Optional[str] = Field(default=None, min_length=1, max_length=255)

    @model_validator(mode="after")
    def validate_payload(self) -> "UpdateUnitRequest":
        if self.name is None:
            raise ValueError("At least one field must be provided")

        return self


class UnitResponsibleAssignmentRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user_id: int = Field(gt=0)
    level: UnitResponsibleLevel


class ReplaceUnitResponsiblesRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    assignments: list[UnitResponsibleAssignmentRequest] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_user_ids(self) -> "ReplaceUnitResponsiblesRequest":
        user_ids = [assignment.user_id for assignment in self.assignments]

        if len(set(user_ids)) != len(user_ids):
            raise ValueError("assignments.user_id must be unique")

        return self
