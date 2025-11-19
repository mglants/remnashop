from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode, StartMode, SubManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Select
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from loguru import logger

from src.bot.states import RemnashopReferral
from src.core.constants import USER_KEY
from src.core.enums import (
    ReferralAccrualStrategy,
    ReferralLevel,
    ReferralRewardStrategy,
    ReferralRewardType,
)
from src.core.utils.formatters import format_user_log as log
from src.infrastructure.database.models.dto import UserDto
from src.services.settings import SettingsService


@inject
async def on_enable_toggle(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
    settings_service: FromDishka[SettingsService],
) -> None:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]

    settings = await settings_service.get()
    settings.referral.enable = not settings.referral.enable
    await settings_service.update(settings)

    logger.info(
        f"{log(user)} Successfully toggled referral system status to '{settings.referral.enable}'"
    )


@inject
async def on_level_select(
    callback: CallbackQuery,
    widget: Select[ReferralLevel],
    dialog_manager: DialogManager,
    selected_level: ReferralLevel,
    settings_service: FromDishka[SettingsService],
) -> None:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    logger.debug(f"{log(user)} Selected referral level '{selected_level}'")

    settings = await settings_service.get()
    settings.referral.level = selected_level
    await settings_service.update(settings)

    logger.info(f"{log(user)} Successfully updated referral level to '{selected_level}'")
    await dialog_manager.switch_to(state=RemnashopReferral.MAIN)


@inject
async def on_reward_select(
    callback: CallbackQuery,
    widget: Select[ReferralRewardType],
    dialog_manager: DialogManager,
    selected_reward: ReferralRewardType,
    settings_service: FromDishka[SettingsService],
) -> None:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    logger.debug(f"{log(user)} Selected referral reward '{selected_reward}'")

    settings = await settings_service.get()
    settings.referral.reward = selected_reward
    await settings_service.update(settings)

    logger.info(f"{log(user)} Successfully updated referral reward to '{selected_reward}'")
    await dialog_manager.switch_to(state=RemnashopReferral.MAIN)


@inject
async def on_accrual_strategy_select(
    callback: CallbackQuery,
    widget: Select[ReferralAccrualStrategy],
    dialog_manager: DialogManager,
    selected_strategy: ReferralAccrualStrategy,
    settings_service: FromDishka[SettingsService],
) -> None:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    logger.debug(f"{log(user)} Selected referral accrual strategy '{selected_strategy}'")

    settings = await settings_service.get()
    settings.referral.accrual_strategy = selected_strategy
    await settings_service.update(settings)

    logger.info(
        f"{log(user)} Successfully updated referral accrual strategy to '{selected_strategy}'"
    )
    await dialog_manager.switch_to(state=RemnashopReferral.MAIN)


@inject
async def on_reward_strategy_select(
    callback: CallbackQuery,
    widget: Select[ReferralRewardStrategy],
    dialog_manager: DialogManager,
    selected_strategy: ReferralRewardStrategy,
    settings_service: FromDishka[SettingsService],
) -> None:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    logger.debug(f"{log(user)} Selected referral reward strategy '{selected_strategy}'")

    settings = await settings_service.get()
    settings.referral.reward_strategy = selected_strategy
    await settings_service.update(settings)

    logger.info(
        f"{log(user)} Successfully updated referral reward strategy to '{selected_strategy}'"
    )
    await dialog_manager.switch_to(state=RemnashopReferral.MAIN)
