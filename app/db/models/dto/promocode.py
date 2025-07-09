from datetime import datetime, timedelta
from typing import Optional

from pydantic import Field

from app.core.enums import PromocodeType
from app.core.utils.time import datetime_now

from .base import TrackableModel


class PromocodeDto(TrackableModel):
    id: Optional[int] = Field(default=None, frozen=True)

    code: str
    type: PromocodeType

    is_active: bool
    is_multi_use: bool

    lifetime: Optional[int] = None
    duration: Optional[int] = None
    traffic: Optional[int] = None
    discount_percent: Optional[int] = None

    activated_by: Optional[int] = None

    created_at: Optional[datetime] = Field(default=None, frozen=True)
    updated_at: Optional[datetime] = Field(default=None, frozen=True)

    @property
    def is_redeemed(self) -> bool:
        return self.activated_by is not None

    @property
    def is_unlimited(self) -> bool:
        return self.lifetime is None

    @property
    def expires_at(self) -> Optional[datetime]:
        if self.lifetime is not None and self.created_at is not None:
            return self.created_at + timedelta(days=self.lifetime)
        return None

    @property
    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False

        current_time = datetime_now()
        return current_time > self.expires_at

    @property
    def time_left(self) -> Optional[timedelta]:
        if self.expires_at is None:
            return None

        current_time = datetime_now()
        delta = self.expires_at - current_time
        return delta if delta.total_seconds() > 0 else timedelta(seconds=0)
