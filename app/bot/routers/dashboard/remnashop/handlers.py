from aiogram.types import CallbackQuery, FSInputFile
from aiogram_dialog import DialogManager, SubManager
from aiogram_dialog.widgets.kbd import Button
from loguru import logger

from app.bot.routers.dashboard.users.user.handlers import (
    handle_role_switch_preconditions,
    reset_user_dialog,
    start_user_window,
)
from app.core.constants import APP_CONTAINER_KEY, LOG_DIR, USER_KEY
from app.core.container import AppContainer
from app.core.enums import MediaType, UserRole
from app.core.logger import LOG_FILENAME
from app.core.utils.formatters import format_log_user
from app.core.utils.time import datetime_now
from app.db.models.dto import UserDto


async def on_logs_requested(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    container: AppContainer = dialog_manager.middleware_data[APP_CONTAINER_KEY]

    try:
        file = FSInputFile(
            path=f"{LOG_DIR}/{LOG_FILENAME}",
            filename=f"{datetime_now().strftime('%Y-%m-%d_%H-%M-%S')}.log",
        )
    except FileNotFoundError:
        logger.error("Log file not found")
        await container.services.notification.notify_user(
            user=user,
            text_key="ntf-error-log-not-found",
        )
        return

    await container.services.notification.notify_user(
        user=user,
        text_key="",
        media=file,
        media_type=MediaType.DOCUMENT,
        auto_delete_after=None,
        add_close_button=True,
    )
    logger.info(f"{format_log_user(user)} Received the log file")


async def on_user_selected(
    callback: CallbackQuery,
    widget: Button,
    sub_manager: SubManager,
) -> None:
    logger.warning(type(sub_manager))
    await start_user_window(manager=sub_manager, target_telegram_id=int(sub_manager.item_id))


async def on_user_role_removed(
    callback: CallbackQuery,
    widget: Button,
    sub_manager: SubManager,
) -> None:
    logger.warning(type(sub_manager))
    await sub_manager.load_data()
    user: UserDto = sub_manager.middleware_data[USER_KEY]
    container: AppContainer = sub_manager.middleware_data[APP_CONTAINER_KEY]
    target_user = await container.services.user.get(telegram_id=int(sub_manager.item_id))

    if not target_user:
        return

    if await handle_role_switch_preconditions(user, target_user, container, sub_manager):
        return

    await container.services.user.set_role(user=target_user, role=UserRole.USER)
    await reset_user_dialog(sub_manager.manager, target_user)
    logger.info(f"{format_log_user(user)} Removed role for {format_log_user(target_user)}")
