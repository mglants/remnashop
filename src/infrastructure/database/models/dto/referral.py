from typing import TYPE_CHECKING, Optional

from src.core.enums import ReferralLevel, ReferralRewardType

if TYPE_CHECKING:
    from .user import BaseUserDto

from datetime import datetime

from pydantic import Field

from .base import TrackableDto


class ReferralDto(TrackableDto):
    id: Optional[int] = Field(default=None, frozen=True)

    level: ReferralLevel

    referrer: "BaseUserDto"
    referred: "BaseUserDto"
    rewards: list["ReferralRewardDto"]

    created_at: Optional[datetime] = Field(default=None, frozen=True)
    updated_at: Optional[datetime] = Field(default=None, frozen=True)


class ReferralRewardDto(TrackableDto):
    id: Optional[int] = Field(default=None, frozen=True)

    reward_type: ReferralRewardType
    reward_amount: int

    # referral: "ReferralDto"
    # user: "UserDto"

    created_at: Optional[datetime] = Field(default=None, frozen=True)
    updated_at: Optional[datetime] = Field(default=None, frozen=True)

    @property
    def rewarded_at(self) -> Optional[datetime]:
        return self.created_at
