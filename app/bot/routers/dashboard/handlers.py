from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select
from loguru import logger

from app.core.constants import APP_CONTAINER_KEY, USER_KEY
from app.core.container import AppContainer
from app.core.enums import MaintenanceMode
from app.core.utils.formatters import format_log_user
from app.db.models.dto import UserDto


async def on_maintenance_mode_selected(
    callback: CallbackQuery,
    widget: Select[MaintenanceMode],
    dialog_manager: DialogManager,
    selected_mode: MaintenanceMode,
) -> None:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    container: AppContainer = dialog_manager.middleware_data[APP_CONTAINER_KEY]

    await container.services.maintenance.set_mode(mode=selected_mode)
    logger.info(f"{format_log_user(user)} Set maintenance mode -> '{selected_mode}'")
