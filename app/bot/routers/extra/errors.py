from aiogram.types import ErrorEvent
from aiogram_dialog import DialogManager
from loguru import logger

from app.bot.routers.menu.handlers import on_start_command
from app.core.container import AppContainer
from app.core.utils.formatters import format_log_user
from app.db.models.dto import UserDto

# NOTE: Registered in main router (app/factories/dispatcher.py)


async def on_unknown_state(
    event: ErrorEvent,
    user: UserDto,
    dialog_manager: DialogManager,
    container: AppContainer,
) -> None:
    logger.error(f"{format_log_user(user)} Unknown state")
    await container.services.notification.notify_user(
        user=user,
        text_key="ntf-error-unknown-state",
    )

    logger.debug(f"{format_log_user(user)} Restarting dialog")
    await on_start_command(message=event.update.message, user=user, dialog_manager=dialog_manager)


async def on_unknown_intent(
    event: ErrorEvent,
    user: UserDto,
    dialog_manager: DialogManager,
    container: AppContainer,
) -> None:
    logger.error(f"{format_log_user(user)} Unknown intent")
    await container.services.notification.notify_user(
        user=user,
        text_key="ntf-error-unknown-intent",
    )

    logger.debug(f"{format_log_user(user)} Restarting dialog")
    await on_start_command(message=event.update.message, user=user, dialog_manager=dialog_manager)
