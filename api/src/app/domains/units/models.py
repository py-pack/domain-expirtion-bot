from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class UnitResponsibleLevel(str, Enum):
    VIEW = "View"
    EDIT = "Edit"
    FULL = "Full"


class Unit(Base):
    __tablename__ = "units"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)


class UnitResponsible(Base):
    __tablename__ = "unit_responsibles"
    __table_args__ = (
        UniqueConstraint("unit_id", "user_id", name="uq_unit_responsibles_unit_user"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    unit_id: Mapped[int] = mapped_column(ForeignKey("units.id", ondelete="CASCADE"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    level: Mapped[UnitResponsibleLevel] = mapped_column(
        SqlEnum(
            UnitResponsibleLevel,
            name="unit_responsible_level",
            values_callable=lambda enum_cls: [item.value for item in enum_cls],
        ),
        nullable=False,
        default=UnitResponsibleLevel.VIEW,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )


@dataclass(frozen=True)
class UnitListItem:
    id: int
    name: str
    responsibles_count: int


@dataclass(frozen=True)
class UnitDetails:
    id: int
    name: str


@dataclass(frozen=True)
class UnitResponsibleUser:
    id: int
    email: str
    full_name: str
    level: str
