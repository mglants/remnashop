from typing import Any

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.core.enums import (
    ReferralAccrualStrategy,
    ReferralLevel,
    ReferralRewardStrategy,
    ReferralRewardType,
)
from src.services.settings import SettingsService


@inject
async def referral_getter(
    dialog_manager: DialogManager,
    settings_service: FromDishka[SettingsService],
    **kwargs: Any,
) -> dict[str, Any]:
    settings = await settings_service.get()

    return {
        "is_enable": settings.referral.enable,
        "referral_level": settings.referral.level,
        "reward_type": settings.referral.reward_type,
        "accrual_strategy": settings.referral.accrual_strategy,
        "reward_strategy": settings.referral.reward_strategy,
    }


async def level_getter(dialog_manager: DialogManager, **kwargs: Any) -> dict[str, Any]:
    return {"levels": list(ReferralLevel)}


async def reward_getter(dialog_manager: DialogManager, **kwargs: Any) -> dict[str, Any]:
    return {"rewards": list(ReferralRewardType)}


async def accrual_strategy_getter(dialog_manager: DialogManager, **kwargs: Any) -> dict[str, Any]:
    return {"strategys": list(ReferralAccrualStrategy)}


async def reward_strategy_getter(dialog_manager: DialogManager, **kwargs: Any) -> dict[str, Any]:
    return {"strategys": list(ReferralRewardStrategy)}
