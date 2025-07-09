from datetime import datetime
from typing import Optional

from pydantic import Field

from app.core.enums import Locale, UserRole
from app.core.utils.time import datetime_now

from .base import TrackableModel


class UserDto(TrackableModel):
    id: Optional[int] = Field(frozen=True)
    telegram_id: int = Field(frozen=True)

    name: str
    role: UserRole = UserRole.USER
    language: Locale

    personal_discount: float = 0
    purchase_discount: float = 0

    is_blocked: bool = False
    is_bot_blocked: bool = False
    is_trial_used: bool = False

    created_at: Optional[datetime] = Field(default=None, frozen=True)
    updated_at: Optional[datetime] = Field(default=None, frozen=True)

    @property
    def is_dev(self) -> bool:
        return self.role == UserRole.DEV

    @property
    def is_admin(self) -> bool:
        return self.role == UserRole.ADMIN

    @property
    def is_privileged(self) -> bool:
        return self.is_admin or self.is_dev

    @property
    def age_days(self) -> Optional[int]:
        if self.created_at is None:
            return None

        current_time = datetime_now()
        return (current_time - self.created_at).days
