import datetime
from enum import StrEnum
from typing import Optional

from sqlalchemy import DateTime, Index
from sqlalchemy.orm import Mapped, mapped_column

from mdm.database.database import Base

class DeviceType(StrEnum):
    android = "android"
    windows = "windows"

class Status(StrEnum):
    active = "active"
    inactive = "inactive"
    offline = "offline"


class Device(Base):
    __tablename__ = "device"
    __table_args__ = (
        Index("idx_device_status_device_type", "status", "device_type"),
    )


    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    device_name: Mapped[str] = mapped_column(unique=False, nullable=False)
    device_type: Mapped[DeviceType] = mapped_column( nullable=False)
    status: Mapped[Status] = mapped_column(nullable=False)
    created_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.datetime.now(),
    )
    last_seen_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=datetime.datetime.now()
    )
    updated_at: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        onupdate=datetime.datetime.now()
    )

    def __str__(self) -> str:
        return (
            f"Device(device_name={self.device_name}, "
            f"device_type={self.device_type}, status={self.status})"
        )

    def __repr__(self) -> str:
        return (
            f"Device(id={self.id}, device_name={self.device_name}, "
            f"device_type={self.device_type}, status={self.status}, "
            f"created_at={self.created_at}, last_seen_at={self.last_seen_at}, "
            f"updated_at={self.updated_at})"
        )


