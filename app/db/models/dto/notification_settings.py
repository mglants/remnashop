from pydantic import Field

from .base import PydanticModel


class SystemNotificationDto(PydanticModel):
    bot_lifetime: bool = Field(default=True)
    user_registered: bool = Field(default=True)
    subscription: bool = Field(default=True)
    promocode_activated: bool = Field(default=True)
    critical_error: bool = Field(default=True)
    system_update: bool = Field(default=True)
    # TODO: torrent_block
    # TODO: traffic_overuse


class UserNotificationDto(PydanticModel):
    # subscription_3_days_left: bool = Field(default=True)
    # subscription_24_hours_left: bool = Field(default=True)
    # subscription_ended: bool = Field(default=True)
    # available_after_maintenance: bool = Field(default=True)
    pass
